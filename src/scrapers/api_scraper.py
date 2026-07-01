"""A lightweight API-based scraper implementation."""

from typing import Any, Dict, Optional
from urllib.request import Request, urlopen

from .base_scraper import BaseScraper


class APIScraper(BaseScraper):
    """Scrape public content by performing a simple HTTP request."""

    def __init__(self, token: str = "", config: Optional[Dict] = None):
        super().__init__(config)
        self.token = token

    def scrape(self, url: str, **kwargs) -> Dict[str, Any]:
        if not self._validate_url(url):
            raise ValueError(f"Invalid Facebook URL: {url}")

        headers = {
            "User-Agent": self.config.get("user_agent", "Mozilla/5.0"),
            "Accept": "application/json, text/plain, */*",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = Request(url, headers=headers)
        response = urlopen(request)
        try:
            content = response.read().decode("utf-8", errors="ignore")
        finally:
            if hasattr(response, "close"):
                response.close()

        return {"url": url, "content": content}

    def close(self):
        return None
