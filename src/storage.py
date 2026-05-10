import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def _timestamp():
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def write_csv(df, name, subdir="processed"):
    out_dir = DATA_DIR / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}_{_timestamp()}.csv"
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"[write] {path} ({len(df)} rows)")
    return path


def write_json_raw(payload, name):
    out_dir = DATA_DIR / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}_{_timestamp()}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def latest(name, subdir="processed"):
    out_dir = DATA_DIR / subdir
    if not out_dir.exists():
        return None
    matches = sorted(out_dir.glob(f"{name}_*.csv"))
    return matches[-1] if matches else None
