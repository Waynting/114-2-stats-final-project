from datetime import datetime, timezone

import pandas as pd

from .common import fetch_videos_by_ids, flatten_video
from .pagination import paginate
from .storage import write_csv


def search_video_ids(client, keyword, quota, max_pages=2, region_code=None,
                     order="viewCount", published_after=None):
    def _builder(token):
        params = dict(
            part="id",
            q=keyword,
            type="video",
            order=order,
            maxResults=50,
        )
        if region_code:
            params["regionCode"] = region_code
        if published_after:
            params["publishedAfter"] = published_after
        if token:
            params["pageToken"] = token
        return client.search().list(**params)

    ids = []
    for item in paginate(_builder, quota=quota, endpoint="search.list", max_pages=max_pages):
        vid = (item.get("id") or {}).get("videoId")
        if vid:
            ids.append(vid)
    return ids


def run(client, config, quota):
    fetched_at = datetime.now(timezone.utc).isoformat()
    keywords = config.get("keywords") or []
    if not keywords:
        raise ValueError("search_top.keywords is empty in config.yaml")

    region = config.get("region_code")
    order = config.get("order", "viewCount")
    published_after = config.get("published_after")
    max_pages = config.get("max_pages_per_keyword", 2)

    rows = []
    for keyword in keywords:
        ids = search_video_ids(
            client,
            keyword,
            quota,
            max_pages=max_pages,
            region_code=region,
            order=order,
            published_after=published_after,
        )
        items = fetch_videos_by_ids(client, ids, quota)
        for item in items:
            row = flatten_video(item)
            row["search_keyword"] = keyword
            row["search_region"] = region
            row["search_order"] = order
            row["fetched_at"] = fetched_at
            rows.append(row)

    df = pd.DataFrame(rows)
    return write_csv(df, "top_by_keyword")
