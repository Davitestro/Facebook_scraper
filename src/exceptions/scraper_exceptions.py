"""Custom exceptions used by the scraper package."""


class ScraperError(Exception):
    """Base scraper exception."""


class ScrapingError(ScraperError):
    """Raised when scraping fails."""


class ValidationError(ScraperError):
    """Raised when incoming input is invalid."""


class ConfigurationError(ScraperError):
    """Raised when scraper configuration is invalid."""
