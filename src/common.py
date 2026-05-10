import isodate

from .pagination import execute


def parse_duration_seconds(iso):
    if not iso:
        return None
    try:
        return int(isodate.parse_duration(iso).total_seconds())
    except Exception:
        return None


def _to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def flatten_video(item):
    snippet = item.get("snippet", {}) or {}
    stats = item.get("statistics", {}) or {}
    content = item.get("contentDetails", {}) or {}
    topic = item.get("topicDetails", {}) or {}
    duration_iso = content.get("duration")
    return {
        "video_id": item.get("id"),
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "channel_id": snippet.get("channelId"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "category_id": _to_int(snippet.get("categoryId")),
        "tags": "|".join(snippet.get("tags", []) or []) or None,
        "default_language": snippet.get("defaultAudioLanguage") or snippet.get("defaultLanguage"),
        "duration_iso": duration_iso,
        "duration_sec": parse_duration_seconds(duration_iso),
        "definition": content.get("definition"),
        "caption": content.get("caption") == "true",
        "view_count": _to_int(stats.get("viewCount")),
        "like_count": _to_int(stats.get("likeCount")),
        "comment_count": _to_int(stats.get("commentCount")),
        "favorite_count": _to_int(stats.get("favoriteCount")),
        "topic_categories": "|".join(topic.get("topicCategories", []) or []) or None,
    }


def fetch_videos_by_ids(client, video_ids, quota,
                        parts="snippet,statistics,contentDetails,topicDetails"):
    seen = set()
    unique_ids = [vid for vid in video_ids if vid and not (vid in seen or seen.add(vid))]
    items = []
    for i in range(0, len(unique_ids), 50):
        batch = unique_ids[i:i + 50]
        if quota:
            quota.charge("videos.list")
        request = client.videos().list(part=parts, id=",".join(batch))
        resp = execute(request)
        items.extend(resp.get("items", []) or [])
    return items


def resolve_channel_ids(client, channel_inputs, quota):
    ids = []
    handles = []
    for entry in channel_inputs:
        if entry.startswith("UC") and len(entry) >= 20:
            ids.append(entry)
        else:
            handles.append(entry.lstrip("@"))
    for handle in handles:
        if quota:
            quota.charge("channels.list")
        request = client.channels().list(part="id", forHandle=handle)
        resp = execute(request)
        for item in resp.get("items", []) or []:
            ids.append(item["id"])
    return ids
