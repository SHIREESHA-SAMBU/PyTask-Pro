# PyTask Pro

**Automated Scripting, Web Scraping & CLI Utility Engine**

A complete Python 3.11 internship project implementing the TechSkillHub assignment requirements: modular OOP architecture, decorators, resilient web scraping with Requests + BeautifulSoup, regex-based cleaning, JSON/CSV file I/O, argparse CLI, unit tests, packaging, and technical documentation.

## Features

- Modular package architecture
- OOP base/concrete classes with encapsulation and inheritance
- `@logged` and `@timed` decorators
- Requests + BeautifulSoup4 scraper
- HTTP error handling, retry logic and 429 rate-limit handling
- Rotating user-agent selection
- Regex-based text cleaning
- JSON and CSV export/import
- `argparse` subcommands
- Pytest test suite
- PEP 8-oriented structure and type hints
- `pyproject.toml` packaging

## Project Structure

```text
PyTaskPro/
├── pytask_pro/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── cli.py
│   ├── exporter.py
│   ├── logger.py
│   ├── models.py
│   └── scraper.py
├── tests/
├── data/
├── output/
├── docs/
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## CLI Usage

Scrape:
```bash
pytask-pro scrape https://books.toscrape.com/ -o output/scraped.json
```

Clean:
```bash
pytask-pro clean output/scraped.json -o output/cleaned.json
```

Export:
```bash
pytask-pro export output/cleaned.json -o output/report.csv
```

Run the full pipeline:
```bash
pytask-pro run https://books.toscrape.com/ --json output/report.json --csv output/report.csv
```

## Testing

```bash
pytest
```

## Responsible scraping

Use only sites that permit automated access, respect robots.txt and terms of service, keep request rates low, and identify your client where appropriate. The included scraper is designed for educational use and a deliberately simple public practice site.

## Assignment mapping

| Requirement | Implementation |
|---|---|
| Python 3.11 | `pyproject.toml` |
| Modular package | `pytask_pro/` |
| OOP | `models.py` |
| Decorators | `logger.py` |
| Requests/BeautifulSoup | `scraper.py` |
| HTTP errors | retry + `raise_for_status()` |
| Rate limiting | delay + 429 handling |
| User-agent rotation | `ScraperConfig` |
| Regex cleaning | `cleaner.py` |
| JSON/CSV | `exporter.py` |
| Argparse | `cli.py` |
| Unit tests | `tests/` |
| Packaging | `pyproject.toml` |
| Documentation | README + PDF report |
| Presentation | PPTX |
| Demo | `docs/video_demo_script.md` |
