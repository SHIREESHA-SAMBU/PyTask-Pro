"""Command-line interface for PyTask Pro."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .cleaner import TextCleaner
from .exporter import DataExporter
from .logger import configure_logging
from .models import Record
from .scraper import ScraperConfig, WebScraper

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pytask-pro",
        description="Automated scripting, scraping, cleaning and export utility.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    scrape = sub.add_parser("scrape", help="Scrape one or more URLs.")
    scrape.add_argument("urls", nargs="+")
    scrape.add_argument("-o", "--output", default="output/scraped.json")
    scrape.add_argument("--delay", type=float, default=1.0)

    clean = sub.add_parser("clean", help="Clean an existing JSON dataset.")
    clean.add_argument("input")
    clean.add_argument("-o", "--output", default="output/cleaned.json")

    export = sub.add_parser("export", help="Convert JSON into CSV.")
    export.add_argument("input")
    export.add_argument("-o", "--output", default="output/report.csv")

    run = sub.add_parser("run", help="Scrape, clean and export in one command.")
    run.add_argument("urls", nargs="+")
    run.add_argument("--json", default="output/report.json")
    run.add_argument("--csv", default="output/report.csv")
    run.add_argument("--delay", type=float, default=1.0)

    return parser

def main(argv: list[str] | None = None) -> int:
    configure_logging()
    args = build_parser().parse_args(argv)
    exporter = DataExporter()

    if args.command == "scrape":
        records = WebScraper(ScraperConfig(delay=args.delay)).scrape(args.urls)
        exporter.to_json(records, args.output)
        print(f"Saved {len(records)} records to {args.output}")

    elif args.command == "clean":
        records = exporter.from_json(args.input)
        records = TextCleaner().clean_records(records)
        exporter.to_json(records, args.output)
        print(f"Cleaned {len(records)} records into {args.output}")

    elif args.command == "export":
        records = exporter.from_json(args.input)
        exporter.to_csv(records, args.output)
        print(f"Exported {len(records)} records to {args.output}")

    elif args.command == "run":
        records = WebScraper(ScraperConfig(delay=args.delay)).scrape(args.urls)
        records = TextCleaner().clean_records(records)
        exporter.to_json(records, args.json)
        exporter.to_csv(records, args.csv)
        print(f"Pipeline complete: {len(records)} records")
        print(json.dumps({"json": args.json, "csv": args.csv}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
