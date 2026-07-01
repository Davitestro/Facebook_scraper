"""Helpers for parsing comment-like content from scraped HTML elements."""

from typing import Any, Dict, Optional


class CommentParser:
    """Parse a comment element or a row dictionary into a normalized dictionary."""

    def parse(self, element: Any, headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        if element is None:
            return None

        if isinstance(element, dict):
            return self._parse_mapping(element, headers=headers, mapping=mapping)

        text = getattr(element, "text", None)
        author = getattr(element, "author", None)
        replies = getattr(element, "replies", None)

        if not text and hasattr(element, "get_attribute"):
            text = element.get_attribute("data-comment") or ""

        if not text:
            return None

        return {
            "comment": str(text).strip(),
            "text": str(text).strip(),
            "author": str(author).strip() if author else None,
            "replies": int(replies) if replies is not None else 0,
        }

    def parse_many(self, elements: list[Any], headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> list[Dict[str, Any]]:
        return [self.parse(element, headers=headers, mapping=mapping) for element in elements]

    def _parse_mapping(self, element: Dict[str, Any], headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        resolved_mapping = mapping or {}
        if headers:
            resolved_mapping = {key: resolved_mapping.get(key, key) for key in headers}

        text_key = resolved_mapping.get("text", "text")
        author_key = resolved_mapping.get("author", "author")
        replies_key = resolved_mapping.get("replies", "replies")

        return {
            "comment": str(element.get(text_key, "")).strip(),
            "text": str(element.get(text_key, "")).strip(),
            "author": str(element.get(author_key, "")).strip() or None,
            "replies": int(element.get(replies_key, 0)) if element.get(replies_key) is not None else 0,
        }
