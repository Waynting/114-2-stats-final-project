# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A YouTube Data API v3 scraping pipeline for a stats course final project. Four research "goals" (`trending`, `channel-compare`, `search-top`, `comments`) each emit timestamped CSVs into `data/processed/` for downstream pandas analysis in `notebooks/`.

`README.md` is the user-facing operating manual (in zh-TW). Read it for the full preset reference, quota costs per endpoint, and category-id table — don't duplicate that here.

## Commands

```bash
source .venv/bin/activate                       # required every new shell
python main.py --list-presets                   # show all presets and which goals each defines
python main.py <goal> [--preset <name>] [--dry-run] [--budget <n>]
```

- `<goal>` ∈ `{trending, channel-compare, search-top, comments}`
- `--preset` defaults to `default` → reads `presets/<name>.yaml`
- `--dry-run` prints the resolved section + quota estimate formula without calling the API; **always run this first** when editing a preset
- `--budget` overrides `quota.per_run_budget` (default 8000, hard ceiling per run)

There is no test suite, linter, or build step. Validate changes by `--dry-run` followed by a small live run (e.g. `trending` is ~12 units).

## Architecture

### Goal → preset → runner dispatch

`main.py` holds a `GOALS` dict mapping CLI goal name → `(preset_section_key, runner_callable)`. A run resolves to:

1. Load `config.yaml` (only `quota.per_run_budget` lives there).
2. Load `presets/<preset>.yaml` and pull out **only** the section matching the goal's `section_key`. A preset file can hold multiple goal sections; unused sections are ignored. Missing section → `KeyError` with a helpful message.
3. Build a `QuotaTracker(budget=...)` and a googleapiclient `youtube` v3 client (API key from `.env` via `python-dotenv`).
4. Call `runner(client, section_config, quota)`.

To add a new goal: write `src/<goal>.py` exporting `run(client, config, quota)`, add an entry to `GOALS` and `DRY_RUN_ESTIMATES` in `main.py`, and add the corresponding section to at least one preset.

### Quota is enforced mid-run, not pre-flight

`src/quota.py` charges per endpoint **before** each API call. If `used + cost > budget`, it raises `QuotaBudgetExceeded`. `main.py` catches that, prints the report, and returns exit code 2. **Runners must call `quota.charge(endpoint)` before every API request** — search through `src/` for `quota.charge(` to see the pattern. Endpoint cost table is in `quota.COSTS`; `search.list` is 100, everything else is 1.

This means a runner can be killed partway through. Anything written to `data/processed/` before the halt is kept; nothing is rolled back. Be aware when adding new runners — write incrementally if a single run produces multiple CSVs that depend on each other.

### Pagination + retry

`src/pagination.py` provides:
- `execute(request)` — wraps `request.execute()` with tenacity retries on HTTP 429/5xx (5 attempts, exponential backoff).
- `paginate(builder, quota, endpoint, max_pages)` — generator that charges quota per page, yields `items`, follows `nextPageToken`. Use this for any list-style endpoint instead of writing a loop.

### Cross-goal CSV chaining

The `comments` goal can resolve `video_ids` either explicitly or via `video_ids_from: trending|top_by_keyword|channel_videos`. When using the second form, `src/storage.latest(name)` globs `data/processed/{name}_*.csv` and picks the lexicographically latest (timestamps are UTC `YYYYMMDD-HHMMSS`, so this == newest). Typical workflow: run `trending` first → run `comments` with `video_ids_from: trending`. Don't break the `<name>_<timestamp>.csv` filename convention — the chaining depends on it.

### Shared helpers

- `src/common.py` — `flatten_video(item)` is the canonical video → row mapper used by `trending`, `channel_compare`, and `search_top`. Keep its output schema stable; downstream notebooks rely on it. `fetch_videos_by_ids` batches in groups of 50 (max for `videos.list`). `resolve_channel_ids` accepts both `UC…` IDs and `@handle` strings.
- `src/storage.py` — `write_csv(df, name)` always appends a UTC timestamp; `latest(name)` reads it back.

## Conventions

- All times stored in CSVs are UTC ISO 8601 strings.
- Integer-ish API fields go through `_to_int` (returns `None` on missing/garbage) — don't trust raw strings from the API.
- API key is read from `.env` (gitignored). Never commit `.env` or hardcode keys.
- Daily quota resets at PT midnight (~Taiwan 15:00). Hitting `403 quotaExceeded` is a wait, not a bug.
