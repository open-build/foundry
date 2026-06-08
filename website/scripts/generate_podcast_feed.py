#!/usr/bin/env python3
"""Generate the FirstCityFoundry podcast RSS feed from one source manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "content" / "podcast" / "feed-source.json"
OUTPUT_PATHS = [
    ROOT / "producer" / "ledger" / "shows" / "foundry" / "feed.xml",
    ROOT / "docs" / "producer" / "ledger" / "shows" / "foundry" / "feed.xml",
]

ATOM_NS = "http://www.w3.org/2005/Atom"
ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
MEDIA_NS = "http://search.yahoo.com/mrss/"

ET.register_namespace("atom", ATOM_NS)
ET.register_namespace("itunes", ITUNES_NS)
ET.register_namespace("media", MEDIA_NS)


def utc_now_rfc2822() -> str:
    return format_datetime(datetime.now(timezone.utc))


def parse_pub_date(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return format_datetime(parsed.astimezone(timezone.utc))


def build_feed(source: dict) -> ET.Element:
    show = source["show"]
    episodes = source.get("episodes", [])

    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
        },
    )
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = show["title"]
    ET.SubElement(channel, "link").text = show["site_url"]
    ET.SubElement(channel, f"{{{ATOM_NS}}}link", {
        "href": show["feed_url"],
        "rel": "self",
        "type": "application/rss+xml",
    })
    ET.SubElement(channel, "description").text = show["description"]
    ET.SubElement(channel, "language").text = show.get("language", "en-us")
    ET.SubElement(channel, "lastBuildDate").text = utc_now_rfc2822()
    ET.SubElement(channel, f"{{{ITUNES_NS}}}author").text = show.get("author", "")
    ET.SubElement(channel, f"{{{ITUNES_NS}}}image", {"href": show["image_url"]})

    for episode in episodes:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = episode["title"]
        ET.SubElement(item, "link").text = episode["link"]
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = episode["guid"]
        ET.SubElement(item, "pubDate").text = parse_pub_date(episode["pub_date"])
        ET.SubElement(item, "description").text = episode["description"]
        ET.SubElement(item, f"{{{ITUNES_NS}}}episode").text = str(episode.get("episode_number", ""))
        if episode.get("image_url"):
            ET.SubElement(item, f"{{{ITUNES_NS}}}image", {"href": episode["image_url"]})

        media_url = episode.get("media_url")
        if media_url:
            media_attrs = {
                "url": media_url,
                "type": episode.get("media_type", "video/mp4"),
                "medium": "video",
            }
            media_length = int(episode.get("media_length") or 0)
            if media_length > 0:
                media_attrs["fileSize"] = str(media_length)
            ET.SubElement(item, "enclosure", {
                "url": media_url,
                "length": str(media_length),
                "type": episode.get("media_type", "video/mp4"),
            })
            ET.SubElement(item, f"{{{MEDIA_NS}}}content", media_attrs)

    return rss


def write_feed(source_path: Path, output_paths: list[Path]) -> None:
    source = json.loads(source_path.read_text())
    feed = build_feed(source)
    xml_text = ET.tostring(feed, encoding="unicode")
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + xml_text + "\n"

    for output_path in output_paths:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_PATH)
    parser.add_argument("--output", type=Path, action="append", default=[])
    args = parser.parse_args()

    outputs = args.output or OUTPUT_PATHS
    write_feed(args.source, outputs)


if __name__ == "__main__":
    main()