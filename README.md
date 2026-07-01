# Facebook Scraper

A comprehensive Facebook scraper built with Python and Selenium that supports infinite scrolling, CAPTCHA handling, and multiple output formats.

## Features

- Infinite scrolling to load all posts
- Manual CAPTCHA solving support
- Progress bar for scraping status
- Post deduplication
- Engagement metrics (likes, comments, shares)
- Image extraction
- Timestamp conversion to ISO format
- Multiple output formats (JSON, CSV)
- Headless mode support
- Anti-detection measures
- Rate limiting

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver compatible with your Chrome version

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/facebook-scraper.git
cd facebook-scraper
```

Install dependencies:

```bash
pip install -r requirements/base.txt
```

For development:

```bash
pip install -r requirements/dev.txt
```

## Configuration

Create a `.env` file in the root directory:

```env
# Facebook Credentials (optional for public pages)
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password_here
FACEBOOK_ACCESS_TOKEN=

# Scraping Settings
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
REQUEST_DELAY=2.0
MAX_RETRIES=3
```

## Usage

### Basic Usage

Scrape a public Facebook page without login:

```bash
python3 -m src.main --url https://www.facebook.com/Reuters --max-posts 500 --no-login --headless
```

### With Login (For Private Content)

```bash
python3 -m src.main --url https://www.facebook.com/your-target-page --max-posts 500
```

This will open a browser window. If a CAPTCHA appears, solve it manually.

### Headless Mode

Run without opening a browser window:

```bash
python3 -m src.main --url https://www.facebook.com/Reuters --max-posts 500 --headless --no-login
```

### Specify Output File

```bash
python3 -m src.main --url https://www.facebook.com/Reuters --max-posts 500 --output data/export/my_data.json --no-login
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Facebook URL to scrape | Required |
| `--max-posts` | Maximum number of posts to scrape | 50 |
| `--output` | Output file path | data/raw/output.json |
| `--headless` | Run browser in headless mode | False |
| `--no-login` | Skip login (for public pages) | False |
| `--method` | Scraping method (selenium/api) | selenium |

## Project Structure

```
facebook-scraper/
├── src/
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuration
│   ├── scrapers/
│   │   ├── base_scraper.py     # Base scraper class
│   │   └── selenium_scraper.py # Selenium implementation
│   ├── parsers/
│   │   └── post_parser.py      # Post data parsing
│   ├── storage/
│   │   └── json_storage.py     # JSON file storage
│   ├── utils/
│   │   ├── logger.py           # Logging setup
│   │   ├── rate_limiter.py     # Rate limiting
│   │   └── cleanup.py          # Data cleanup utilities
│   └── exceptions/
│       └── scraper_exceptions.py
├── data/
│   ├── raw/                    # Raw scraped data
│   ├── processed/              # Processed data
│   └── exports/                # Exported files
├── logs/                       # Log files
├── config/                     # Configuration files
├── requirements/
│   ├── base.txt                # Base requirements
│   └── dev.txt                 # Development requirements
├── .env                        # Environment variables
└── README.md                   # This file
```

## Data Output Format

The scraper outputs data in JSON format:

```json
{
  "metadata": {
    "scraped_at": "2026-07-01T20:36:35.906285",
    "total_items": 1
  },
  "data": {
    "url": "https://www.facebook.com/Reuters",
    "posts": [
      {
        "post_id": "1234567890",
        "author": "Reuters",
        "text": "Post content here...",
        "full_text": "Full post content here...",
        "publish_date": "2026-07-01T20:36:23.161208",
        "timestamp_iso": "2026-07-01T20:36:23.161208",
        "link": "https://www.facebook.com/...",
        "likes": 49,
        "comments": 0,
        "shares": 0,
        "images": ["https://...jpg"],
        "has_video": false,
        "hashtags": ["#example"],
        "mentions": ["@user"],
        "word_count": 14,
        "char_count": 93,
        "scraped_at": "2026-07-01T20:36:35.906045"
      }
    ],
    "total_found": 1,
    "type": "page",
    "page_title": "Reuters | Facebook"
  },
  "scraping_metadata": {
    "scraped_at": "2026-07-01T20:36:35.906244",
    "method": "selenium",
    "max_posts": 500,
    "url": "https://www.facebook.com/Reuters",
    "login_used": false
  }
}
```

## CAPTCHA Handling

When running without `--headless` mode, the scraper will:

1. Open a browser window
2. Fill in login credentials
3. Detect if a CAPTCHA is present
4. Wait for you to solve the CAPTCHA manually
5. Continue scraping automatically after solving

You have 180 seconds to solve the CAPTCHA.

## Rate Limiting

The scraper includes built-in rate limiting to avoid detection:

- Minimum delay between requests: 1 second
- Exponential backoff on failures
- Random scrolling patterns
- Human-like behavior simulation

## Docker Support

Build the Docker image:

```bash
docker-compose build
```

Run with Docker:

```bash
docker-compose run --rm scraper python -m src.main --url https://www.facebook.com/Reuters --max-posts 500 --no-login --headless
```

## Logging

Logs are written to:

- Console output
- `logs/scraper.log` file

Log levels:
- INFO: General progress information
- WARNING: Non-critical issues
- ERROR: Critical failures

## Troubleshooting

### Login Failed

If login fails:

1. Check your credentials in `.env`
2. Try running without `--headless` to see the browser
3. Check if Facebook requires additional verification
4. Use `--no-login` for public pages

### No Posts Found

If no posts are scraped:

1. The page might require login
2. The URL might be incorrect
3. Facebook might have changed their layout
4. Try using `--no-login` for public pages

### CAPTCHA Loop

If CAPTCHA keeps appearing:

1. The session might be flagged
2. Try using a different IP/proxy
3. Reduce request frequency
4. Use `--no-login` for public content

## Legal Disclaimer

This tool is for educational purposes only. Facebook's Terms of Service prohibit scraping. Use this tool responsibly and only on content you have permission to access.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Selenium WebDriver
- tqdm for progress bars
- Python community