"""Resilient web scraping engine."""
from __future__ import annotations
import random
import time
from dataclasses import dataclass
from typing import Iterable
import requests
from bs4 import BeautifulSoup
from .logger import logged, timed
from .models import Record

@dataclass
class ScraperConfig:
    timeout: float = 15.0
    delay: float = 1.0
    max_retries: int = 3
    user_agents: tuple[str, ...] = (
        "PyTaskPro/1.0 (+educational scraper)",
        "Mozilla/5.0 (compatible; PyTaskPro/1.0)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    )

class WebScraper:
    """Scrape product cards from a compatible HTML page."""
    def __init__(self, config: ScraperConfig | None = None):
        self.config = config or ScraperConfig()
        self.session = requests.Session()

    def _headers(self) -> dict[str, str]:
        return {"User-Agent": random.choice(self.config.user_agents)}

    @logged
    def fetch(self, url: str) -> str:
        last_error: Exception | None = None
        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = self.session.get(
                    url, headers=self._headers(), timeout=self.config.timeout
                )
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "2"))
                    time.sleep(min(retry_after, 10))
                    continue
                response.raise_for_status()
                return response.text
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.config.max_retries:
                    time.sleep(min(self.config.delay * attempt, 5))
        raise RuntimeError(f"Unable to fetch {url}: {last_error}") from last_error

    @timed
    def parse(self, html: str, source_url: str = "") -> list[Record]:
        soup = BeautifulSoup(html, "html.parser")
        records: list[Record] = []
        for card in soup.select("article.product_pod"):
            title_el = card.select_one("h3 a")
            price_el = card.select_one(".price_color")
            rating_el = card.select_one(".star-rating")
            avail_el = card.select_one(".availability")
            if title_el:
                records.append(
                    Record(
                        title=title_el.get("title", title_el.get_text(" ", strip=True)),
                        price=price_el.get_text(" ", strip=True) if price_el else "",
                        rating=" ".join(rating_el.get("class", [])[1:]) if rating_el else "",
                        availability=avail_el.get_text(" ", strip=True) if avail_el else "",
                        source_url=source_url,
                    )
                )
        return records

    def scrape(self, urls: Iterable[str]) -> list[Record]:
        results: list[Record] = []
        for url in urls:
            html = self.fetch(url)
            results.extend(self.parse(html, url))
            time.sleep(self.config.delay)
        return results
