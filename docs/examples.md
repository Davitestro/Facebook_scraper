# Examples

## Run the CLI

```bash
python -m src.main --method selenium --url https://www.facebook.com/facebook --headless
```

## Use the API scraper

```python
from src.scrapers.api_scraper import APIScraper

scraper = APIScraper(token="demo-token")
result = scraper.scrape("https://www.facebook.com/example")
print(result["url"])
print(result["content"][:200])
```

## Save data as JSON

```python
from src.scrapers.selenium_scraper import SeleniumScraper
from src.storage.json_storage import JSONStorage

scraper = SeleniumScraper(headless=True)
data = scraper.scrape("https://www.facebook.com/facebook")
JSONStorage("data/raw/example.json").save(data)
scraper.close()
```

## Save data as CSV

```python
from src.storage.csv_storage import CSVStorage

rows = [{"text": "Hello", "likes": 5}]
CSVStorage("data/exports/example.csv", fieldnames=["text", "likes"]).save(rows)
```

## Use the database storage

```python
from src.storage.database import DatabaseStorage

storage = DatabaseStorage(connection=":memory:")
storage.save({"text": "Hello from SQLite"})
print(storage.load())
```
