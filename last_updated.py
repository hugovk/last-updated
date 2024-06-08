#!/usr/bin/env python3
"""
Calculate the number of hours since the Python documentation was last updated.
"""

import datetime as dt
import re

import urllib3

HEADERS = {"Cache-Control": "no-cache"}
LAST_UPDATED_ON = re.compile(
    r"Last updated on (\w{3} \d{2}, \d{4}) \((\d{2}:\d{2} UTC)\)"
)
http = urllib3.PoolManager()


def get_html(version: str) -> str:
    url = f"https://docs.python.org/{version}/"
    response = http.request("GET", url, headers=HEADERS)
    return response.data.decode("utf-8")


def find_last_updated(html: str) -> dt.datetime | None:
    for line in html.splitlines():
        if m := re.search(LAST_UPDATED_ON, line):
            date_str, time_str = m.groups()
            date = dt.datetime.strptime(
                f"{date_str} {time_str}", "%b %d, %Y %H:%M %Z"
            ).replace(tzinfo=dt.UTC)
            return date

    return None


def calc_hours_since(date: dt.datetime) -> float | None:
    now = dt.datetime.now(dt.UTC)
    diff = now - date
    hours = diff.total_seconds() / 3600
    return hours


def do_version(version: str, csv: bool = False) -> None:
    html = get_html(version)
    date = find_last_updated(html)
    if not date:
        if not csv:
            print(f"{version}: Unable to find last updated date")
        return

    if csv:
        print(f"{version},{date.isoformat()}")
    else:
        hours = calc_hours_since(date)
        print(
            f"{version}: "
            f"Last updated on {date.strftime('%b %d, %Y (%H:%M UTC)')}"
            f" - {hours:.1f} hours ago"
        )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--versions",
        default="3.12,3.13,3.14",
        help="comma-separated versions",
    )
    parser.add_argument("--csv", action="store_true", help="output as CSV")
    args = parser.parse_args()

    if not args.csv:
        print(
            "Now:                 ",
            dt.datetime.now(dt.UTC).strftime("%b %d, %Y (%H:%M UTC)"),
        )

    for version in args.versions.split(","):
        do_version(version, args.csv)


if __name__ == "__main__":
    main()
