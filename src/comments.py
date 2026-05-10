from datetime import datetime, timezone

import pandas as pd
from googleapiclient.errors import HttpError

from .pagination import paginate
from .storage import latest, write_csv


def _to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _flatten_top_comment(thread, video_id):
    top = (((thread.get("snippet") or {}).get("topLevelComment") or {}).get("snippet")) or {}
    return {
        "video_id": video_id,
        "comment_id": (((thread.get("snippet") or {}).get("topLevelComment") or {}).get("id")),
        "author_display_name": top.get("authorDisplayName"),
        "author_channel_id": ((top.get("authorChannelId") or {}).get("value")),
        "text": top.get("textOriginal") or top.get("textDisplay"),
        "like_count": _to_int(top.get("likeCount")),
        "published_at": top.get("publishedAt"),
        "updated_at": top.get("updatedAt"),
        "total_reply_count": _to_int((thread.get("snippet") or {}).get("totalReplyCount")),
    }


def _flatten_reply(reply, parent_id):
    s = reply.get("snippet") or {}
    return {
        "parent_id": parent_id,
        "comment_id": reply.get("id"),
        "author_display_name": s.get("authorDisplayName"),
        "author_channel_id": ((s.get("authorChannelId") or {}).get("value")),
        "text": s.get("textOriginal") or s.get("textDisplay"),
        "like_count": _to_int(s.get("likeCount")),
        "published_at": s.get("publishedAt"),
        "updated_at": s.get("updatedAt"),
    }


def fetch_replies(client, parent_id, quota, max_pages=5):
    def _builder(token):
        params = dict(
            part="snippet",
            parentId=parent_id,
            maxResults=100,
            textFormat="plainText",
        )
        if token:
            params["pageToken"] = token
        return client.comments().list(**params)

    rows = []
    for item in paginate(_builder, quota=quota, endpoint="comments.list", max_pages=max_pages):
        rows.append(_flatten_reply(item, parent_id))
    return rows


def fetch_comments_for_video(client, video_id, quota, max_pages=5,
                             order="relevance", fetch_extra_replies=False):
    def _builder(token):
        params = dict(
            part="snippet,replies",
            videoId=video_id,
            maxResults=100,
            order=order,
            textFormat="plainText",
        )
        if token:
            params["pageToken"] = token
        return client.commentThreads().list(**params)

    top_rows = []
    reply_rows = []
    for thread in paginate(_builder, quota=quota, endpoint="commentThreads.list", max_pages=max_pages):
        top_row = _flatten_top_comment(thread, video_id)
        top_rows.append(top_row)
        inline = ((thread.get("replies") or {}).get("comments")) or []
        for reply in inline:
            reply_rows.append(_flatten_reply(reply, top_row["comment_id"]))
        if fetch_extra_replies and top_row["total_reply_count"] and top_row["total_reply_count"] > len(inline):
            extra = fetch_replies(client, top_row["comment_id"], quota)
            existing = {r["comment_id"] for r in reply_rows if r["parent_id"] == top_row["comment_id"]}
            for r in extra:
                if r["comment_id"] not in existing:
                    reply_rows.append(r)
    return top_rows, reply_rows


def _resolve_video_ids(config):
    explicit = config.get("video_ids")
    if explicit:
        return list(explicit)
    source = config.get("video_ids_from")
    if not source:
        return []
    path = latest(source)
    if not path:
        raise FileNotFoundError(f"No CSV found for source '{source}' in data/processed")
    df = pd.read_csv(path)
    if "video_id" not in df.columns:
        raise ValueError(f"{path} has no 'video_id' column")
    limit = config.get("limit")
    ids = df["video_id"].dropna().astype(str).tolist()
    return ids[:limit] if limit else ids


def run(client, config, quota):
    fetched_at = datetime.now(timezone.utc).isoformat()
    video_ids = _resolve_video_ids(config)
    if not video_ids:
        raise ValueError("comments: no video_ids resolved (set comments.video_ids or comments.video_ids_from)")

    max_pages = config.get("max_pages_per_video", 5)
    order = config.get("order", "relevance")
    fetch_extra = config.get("fetch_replies", False)

    all_top, all_replies, skipped = [], [], []
    for vid in video_ids:
        try:
            top_rows, reply_rows = fetch_comments_for_video(
                client, vid, quota,
                max_pages=max_pages, order=order, fetch_extra_replies=fetch_extra,
            )
            all_top.extend(top_rows)
            all_replies.extend(reply_rows)
        except HttpError as exc:
            status = getattr(exc.resp, "status", None)
            reason = str(exc)
            skipped.append({"video_id": vid, "status": status, "reason": reason})
            print(f"[skip] {vid}: status={status} reason={reason[:120]}")
            if status in (401, 403) and "quotaExceeded" in reason:
                raise

    top_df = pd.DataFrame(all_top)
    if not top_df.empty:
        top_df["fetched_at"] = fetched_at
    replies_df = pd.DataFrame(all_replies)
    if not replies_df.empty:
        replies_df["fetched_at"] = fetched_at
    skipped_df = pd.DataFrame(skipped)

    paths = [write_csv(top_df, "comments_top")]
    if not replies_df.empty:
        paths.append(write_csv(replies_df, "comments_replies"))
    if not skipped_df.empty:
        paths.append(write_csv(skipped_df, "comments_skipped"))
    return paths
