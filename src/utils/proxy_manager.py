"""Utility helpers for managing a pool of proxies."""

import os
from typing import List, Optional


class ProxyManager:
    """Load and rotate proxies from a configured file."""

    def __init__(self, proxy_file: Optional[str] = None):
        self.proxy_file = proxy_file or os.path.join("config", "proxies.txt")
        self.proxies = self._load_proxies()
        self._index = 0

    def _load_proxies(self) -> List[str]:
        if not os.path.exists(self.proxy_file):
            return []

        with open(self.proxy_file, "r", encoding="utf-8") as handle:
            return [line.strip() for line in handle if line.strip()]

    def get_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None

        proxy = self.proxies[self._index % len(self.proxies)]
        self._index += 1
        return proxy

    def reset(self) -> None:
        self._index = 0
