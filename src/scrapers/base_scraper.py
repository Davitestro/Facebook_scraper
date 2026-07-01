"""
Base Scraper Abstract Class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = logger
        
    @abstractmethod
    def scrape(self, url: str, **kwargs) -> Dict[str, Any]:
        """Scrape data from given URL"""
        pass
    
    @abstractmethod
    def close(self):
        """Clean up resources"""
        pass
    
    def _validate_url(self, url: str) -> bool:
        """Validate Facebook URL"""
        return 'facebook.com' in url or 'fb.com' in url

    def parse_rows(self, rows: list[dict], parser: Any, headers: Optional[list[str]] = None, mapping: Optional[dict] = None) -> list[dict]:
        """Parse a list of row dictionaries using the supplied parser."""
        return parser.parse_many(rows, headers=headers, mapping=mapping)
    
    def _handle_error(self, error: Exception, context: str):
        """Handle errors gracefully"""
        self.logger.error(f"{context}: {str(error)}")
        raise