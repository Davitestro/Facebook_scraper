"""Helpers for parsing profile-like content from scraped HTML elements."""

from typing import Any, Dict, Optional


class ProfileParser:
    """Parse a profile element or a row dictionary into a normalized dictionary."""

    def parse(self, element: Any, headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        if element is None:
            return None

        if isinstance(element, dict):
            return self._parse_mapping(element, headers=headers, mapping=mapping)

        name = getattr(element, "name", None)
        bio = getattr(element, "bio", None)

        if not name and hasattr(element, "get_attribute"):
            name = element.get_attribute("title") or element.get_attribute("data-name") or ""

        if not name:
            return None

        return {
            "name": str(name).strip(),
            "bio": str(bio).strip() if bio else None,
        }

    def parse_many(self, elements: list[Any], headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> list[Dict[str, Any]]:
        return [self.parse(element, headers=headers, mapping=mapping) for element in elements]

    def _parse_mapping(self, element: Dict[str, Any], headers: Optional[list[str]] = None, mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        resolved_mapping = mapping or {}
        if headers:
            resolved_mapping = {key: resolved_mapping.get(key, key) for key in headers}

        name_key = resolved_mapping.get("name", "name")
        bio_key = resolved_mapping.get("bio", "bio")

        return {
            "name": str(element.get(name_key, "")).strip(),
            "bio": str(element.get(bio_key, "")).strip() or None,
        }
