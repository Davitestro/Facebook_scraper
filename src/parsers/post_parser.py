"""Helpers for parsing post-like content from scraped HTML elements."""

import re
from typing import Any, Dict, Optional


class PostParser:
    """Parse a post element or a row dictionary into a normalized dictionary."""

    def parse(self, element: Any, headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        if element is None:
            return None

        if isinstance(element, dict):
            return self._parse_mapping(element, headers=headers, mapping=mapping)

        text = getattr(element, "text", None)
        if text is None and hasattr(element, "get_attribute"):
            text = element.get_attribute("title") or element.get_attribute("data-content") or ""

        if not text:
            return None

        return {
            "text": str(text).strip(),
            "likes": self._coerce_count(getattr(element, "likes", None)),
            "comments": self._coerce_count(getattr(element, "comments", None)),
            "shares": self._coerce_count(getattr(element, "shares", None)),
        }

    def parse_many(self, elements: list[Any], headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> list[Dict[str, Any]]:
        return [self.parse(element, headers=headers, mapping=mapping) for element in elements]

    def _parse_mapping(self, element: Dict[str, Any], headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        resolved_mapping = mapping or {}
        if headers:
            resolved_mapping = {key: resolved_mapping.get(key, key) for key in headers}

        text_key = resolved_mapping.get("text", "text")
        likes_key = resolved_mapping.get("likes", "likes")
        comments_key = resolved_mapping.get("comments", "comments")
        shares_key = resolved_mapping.get("shares", "shares")

        return {
            "text": str(element.get(text_key, "")).strip(),
            "likes": self._coerce_count(element.get(likes_key)),
            "comments": self._coerce_count(element.get(comments_key)),
            "shares": self._coerce_count(element.get(shares_key)),
        }

    def _coerce_count(self, value: Any) -> int:
        if value is None:
            return 0
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            match = re.search(r"(\d+)", value)
            if match:
                return int(match.group(1))
        return 0
