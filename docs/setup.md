# Setup Guide

## 1. Prerequisites

- Python 3.10+
- pip
- Chrome or Chromium installed for Selenium-based scraping
- Optional: Docker and Docker Compose

## 2. Clone the repository

```bash
git clone <your-repo-url>
cd scrapper
```

## 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

## 5. Configure environment variables

Create a `.env` file with values such as:

```env
FACEBOOK_EMAIL=your-email
FACEBOOK_PASSWORD=your-password
FACEBOOK_ACCESS_TOKEN=your-token
```

## 6. Run the scraper

```bash
python -m src.main --method selenium --url https://www.facebook.com/facebook --headless
```

## 7. Docker setup

```bash
docker-compose build
docker-compose up
```

## 8. Notes

- The Selenium scraper requires ChromeDriver-compatible browser support.
- The API scraper can work without a browser, but its functionality is intentionally lightweight.
- Keep the proxy and user-agent lists in the `config/` directory if you want to rotate them.
