"""
Calculate the time between updates for different versions of the Python docs.
"""

import csv
import datetime as dt
from collections import defaultdict

from rich import print

from last_updated import calc_hours_since

last_updated = defaultdict(list)
with open("last_updated.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        version = row["version"]
        timestamp = row["timestamp"]
        last_updated[version].append(timestamp)


print("Time between deploys; last one is time since last deploy:")
for version in sorted(last_updated):
    timestamps = last_updated[version]
    timestamps = [dt.datetime.fromisoformat(ts) for ts in timestamps]
    # Time between each deploy
    diffs = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
    # As hours
    diffs = [(diff.total_seconds() / 3600) for diff in diffs]
    # Last one is time since last update
    diffs.append(calc_hours_since(timestamps[-1]))
    diffs = [f"{diff:.1f} hours" for diff in diffs]
    diffs[-1] = diffs[-1] + " ago"
    print(f"Version {version}: {diffs}")
