from datetime import datetime, timezone

import pandas as pd

from .common import flatten_video
from .pagination import paginate
from .storage import write_csv


def fetch_trending(client, regions, category_ids=None, quota=None, max_per_region=200):
    snapshot_at = datetime.now(timezone.utc).isoformat()
    rows = []
    cats = category_ids if category_ids else [None]
    max_pages = max(1, max_per_region // 50)

    for region in regions:
        for cat in cats:
            rank = 1

            def _builder(token, region=region, cat=cat):
                params = dict(
                    part="snippet,statistics,contentDetails,topicDetails",
                    chart="mostPopular",
                    regionCode=region,
                    maxResults=50,
                )
                if cat is not None:
                    params["videoCategoryId"] = str(cat)
                if token:
                    params["pageToken"] = token
                return client.videos().list(**params)

            for item in paginate(_builder, quota=quota, endpoint="videos.list", max_pages=max_pages):
                row = flatten_video(item)
                row["region_code"] = region
                row["category_filter"] = cat
                row["rank"] = rank
                row["snapshot_at"] = snapshot_at
                rows.append(row)
                rank += 1

    return pd.DataFrame(rows)


def run(client, config, quota):
    df = fetch_trending(
        client,
        regions=config["regions"],
        category_ids=config.get("category_ids"),
        quota=quota,
        max_per_region=config.get("max_per_region", 200),
    )
    return write_csv(df, "trending")
