import argparse
import sys
from pathlib import Path

import yaml

from src import channel_compare, comments, search_top, trending
from src.client import build_data_client
from src.quota import QuotaBudgetExceeded, QuotaTracker

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"
PRESETS_DIR = ROOT / "presets"

GOALS = {
    "search-top": ("search_top", search_top.run),
    "channel-compare": ("channel_compare", channel_compare.run),
    "trending": ("trending", trending.run),
    "comments": ("comments", comments.run),
}

DRY_RUN_ESTIMATES = {
    "search-top": "100 * (keywords * max_pages_per_keyword) + 1 * ceil(total_video_ids / 50)",
    "channel-compare": "1 * ceil(channels / 50) + (1 * pages_per_uploads * channels) + 1 * ceil(total_videos / 50)",
    "trending": "1 * regions * categories * ceil(max_per_region / 50)",
    "comments": "1 * (videos * max_pages_per_video) [+ comments.list if fetch_replies]",
}


def load_yaml(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def list_presets():
    if not PRESETS_DIR.exists():
        return []
    return sorted(p.stem for p in PRESETS_DIR.glob("*.yaml"))


def resolve_preset(name):
    path = PRESETS_DIR / f"{name}.yaml"
    if not path.exists():
        available = ", ".join(list_presets()) or "(none)"
        raise FileNotFoundError(
            f"Preset '{name}' not found at {path}. Available: {available}"
        )
    return path


def load_section(goal, preset_name):
    section_key = GOALS[goal][0]
    preset_path = resolve_preset(preset_name)
    preset = load_yaml(preset_path)
    if section_key not in preset:
        raise KeyError(
            f"Preset '{preset_name}' has no '{section_key}' section. "
            f"Add it to {preset_path} or pick a different preset."
        )
    return preset[section_key], preset_path


def main():
    parser = argparse.ArgumentParser(description="YouTube Data API v3 scraping pipeline")
    parser.add_argument("goal", nargs="?", choices=list(GOALS.keys()),
                        help="Which goal to run")
    parser.add_argument("--preset", default="default",
                        help="Preset name from presets/<name>.yaml (default: 'default')")
    parser.add_argument("--list-presets", action="store_true",
                        help="List available presets and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show quota estimate and resolved config without calling the API")
    parser.add_argument("--budget", type=int, default=None,
                        help="Override quota.per_run_budget for this run")
    args = parser.parse_args()

    if args.list_presets:
        names = list_presets()
        if not names:
            print("(no presets found in presets/)")
            return 0
        print("Available presets:")
        for name in names:
            path = PRESETS_DIR / f"{name}.yaml"
            preset = load_yaml(path)
            goals_in_preset = ", ".join(sorted(preset.keys())) or "(empty)"
            print(f"  {name:<20s} -> {goals_in_preset}")
        return 0

    if not args.goal:
        parser.error("goal is required (or use --list-presets)")

    config = load_yaml(CONFIG_PATH)
    section_config, preset_path = load_section(args.goal, args.preset)

    if args.dry_run:
        print(f"Dry run for goal '{args.goal}' with preset '{args.preset}':")
        print(f"  preset file:      {preset_path}")
        print(f"  estimate formula: {DRY_RUN_ESTIMATES[args.goal]}")
        print(f"  resolved config:  {section_config}")
        print(f"  budget:           {args.budget or config.get('quota', {}).get('per_run_budget', 8000)}")
        return 0

    budget = args.budget or config.get("quota", {}).get("per_run_budget", 8000)
    quota = QuotaTracker(budget=budget)

    runner = GOALS[args.goal][1]
    print(f"[run] goal={args.goal} preset={args.preset} budget={budget}")
    client = build_data_client()
    try:
        runner(client, section_config, quota)
    except QuotaBudgetExceeded as exc:
        print(f"[halt] {exc}", file=sys.stderr)
        print(quota.report(), file=sys.stderr)
        return 2
    finally:
        print(quota.report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
