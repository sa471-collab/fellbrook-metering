from collections import defaultdict
from datetime import timezone


def bucket_for(ts):
    """The UTC hour an event is billed in, e.g. 2026-11-03T14."""
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H")


def totals_by_bucket(events):
    """events is a list of (timestamp, units). Returns {bucket: units}."""
    totals = defaultdict(int)
    for ts, units in events:
        totals[bucket_for(ts)] += units
    return dict(totals)


def export_csv(totals):
    return "\n".join(f"{bucket},{units}" for bucket, units in sorted(totals.items()))
