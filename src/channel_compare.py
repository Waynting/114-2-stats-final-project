from datetime import datetime, timezone

import pandas as pd

from .common import fetch_videos_by_ids, flatten_video, resolve_channel_ids
from .pagination import execute, paginate
from .storage import write_csv


def _to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _flatten_channel(item):
    snippet = item.get("snippet", {}) or {}
    stats = item.get("statistics", {}) or {}
    content = item.get("contentDetails", {}) or {}
    uploads = (content.get("relatedPlaylists", {}) or {}).get("uploads")
    return {
        "channel_id": item.get("id"),
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "custom_url": snippet.get("customUrl"),
        "country": snippet.get("country"),
        "published_at": snippet.get("publishedAt"),
        "view_count": _to_int(stats.get("viewCount")),
        "subscriber_count": _to_int(stats.get("subscriberCount")),
        "hidden_subscriber_count": stats.get("hiddenSubscriberCount", False),
        "video_count": _to_int(stats.get("videoCount")),
        "uploads_playlist_id": uploads,
    }


def fetch_channels(client, channel_ids, quota):
    items = []
    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i:i + 50]
        quota.charge("channels.list")
        request = client.channels().list(
            part="snippet,statistics,contentDetails",
            id=",".join(batch),
        )
        resp = execute(request)
        items.extend(resp.get("items", []) or [])
    return items


def fetch_uploads_video_ids(client, uploads_playlist_id, quota, max_videos):
    max_pages = max(1, (max_videos + 49) // 50)

    def _builder(token):
        params = dict(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
        )
        if token:
            params["pageToken"] = token
        return client.playlistItems().list(**params)

    ids = []
    for item in paginate(_builder, quota=quota, endpoint="playlistItems.list", max_pages=max_pages):
        vid = (item.get("contentDetails", {}) or {}).get("videoId")
        if vid:
            ids.append(vid)
        if len(ids) >= max_videos:
            break
    return ids[:max_videos]


def run(client, config, quota):
    fetched_at = datetime.now(timezone.utc).isoformat()
    inputs = config.get("channel_ids") or []
    if not inputs:
        raise ValueError("channel_compare.channel_ids is empty in config.yaml")
    max_videos = config.get("max_videos_per_channel", 200)

    channel_ids = resolve_channel_ids(client, inputs, quota)
    channel_items = fetch_channels(client, channel_ids, quota)
    channel_rows = []
    for ch in channel_items:
        row = _flatten_channel(ch)
        row["fetched_at"] = fetched_at
        channel_rows.append(row)
    channels_df = pd.DataFrame(channel_rows)

    all_video_ids = []
    channel_for_video = {}
    for row in channel_rows:
        uploads = row.get("uploads_playlist_id")
        if not uploads:
            continue
        vids = fetch_uploads_video_ids(client, uploads, quota, max_videos)
        for vid in vids:
            channel_for_video[vid] = row["channel_id"]
            all_video_ids.append(vid)

    video_items = fetch_videos_by_ids(client, all_video_ids, quota)
    video_rows = []
    for item in video_items:
        row = flatten_video(item)
        row["fetched_at"] = fetched_at
        video_rows.append(row)
    videos_df = pd.DataFrame(video_rows)

    channels_path = write_csv(channels_df, "channels")
    videos_path = write_csv(videos_df, "channel_videos")
    return channels_path, videos_path
