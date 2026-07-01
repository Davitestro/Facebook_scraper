"""Validation helpers for scraper inputs."""

import re
from typing import Optional


def is_valid_facebook_url(url: Optional[str]) -> bool:
    if not url:
        return False
    return "facebook.com" in url or "fb.com" in url


def validate_email(email: Optional[str]) -> bool:
    if not email:
        return False
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def validate_password(password: Optional[str]) -> bool:
    return bool(password and len(password) >= 6)
