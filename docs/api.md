# API Reference

## Core classes

### Config

The `Config` dataclass loads environment values and exposes defaults for scraper behavior.

Example:

```python
from src.config import Config

config = Config()
print(config.ACCESS_TOKEN)
```

### BaseScraper

Base class for all scraper implementations. It provides URL validation and error handling hooks.

### APIScraper

A lightweight HTTP-based scraper that performs a request and returns the HTML/text body.

```python
from src.scrapers.api_scraper import APIScraper

scraper = APIScraper(token="demo-token")
result = scraper.scrape("https://www.facebook.com/example")
print(result["content"])
```

### SeleniumScraper

Browser-based scraper using Selenium and a Chrome driver.

```python
from src.scrapers.selenium_scraper import SeleniumScraper

scraper = SeleniumScraper(headless=True)
result = scraper.scrape("https://www.facebook.com/facebook")
scraper.close()
```

## Parsers

- `PostParser`: parses post-like payloads into a normalized dictionary.
- `CommentParser`: parses comment entries.
- `ProfileParser`: parses profile metadata.

## Storage backends

- `JSONStorage`: writes JSON files with metadata.
- `CSVStorage`: writes rows to CSV files.
- `DatabaseStorage`: persists payloads in SQLite.

## Utilities

- `setup_logger()`: creates a logger for console and file output.
- `ProxyManager`: rotates proxy values from `config/proxies.txt`.
- `UserAgentManager`: rotates user agents from `config/user_agents.txt`.
- `validate_email()`, `validate_password()`, and `is_valid_facebook_url()`: input helpers.
