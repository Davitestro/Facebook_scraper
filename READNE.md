# Facebook Scraper

A comprehensive Facebook scraper built with Python and Selenium.

## Features
- Profile scraping
- Post scraping
- Comment extraction
- Multiple output formats (JSON, CSV)
- Rate limiting
- Proxy support
- Docker support

## Installation

\`\`\`bash
# Clone repository
git clone https://github.com/yourusername/facebook-scraper.git
cd facebook-scraper

# Install dependencies
pip install -r requirements/base.txt

# Copy environment file
cp .env.example .env
# Edit .env with your credentials
\`\`\`

## Usage

\`\`\`bash
# Basic usage
python -m src.main --url https://www.facebook.com/facebook

# With options
python -m src.main --method selenium --url https://www.facebook.com/facebook --output data/export.json --headless
\`\`\`

## Docker Usage

\`\`\`bash
# Build image
docker-compose build

# Run scraper
docker-compose run --rm scraper python -m src.main --url https://www.facebook.com/facebook
\`\`\`

## Legal Disclaimer
This tool is for educational purposes only. Always respect Facebook's Terms of Service.
\`\`\`

---

## How to Use This Structure

1. **Clone/Create the structure**:
```bash
mkdir facebook-scraper
cd facebook-scraper
mkdir -p src/{scrapers,parsers,storage,utils,exceptions}
mkdir -p tests/{test_scrapers,test_parsers,test_utils}
mkdir -p data/{raw,processed,exports}
mkdir -p logs config scripts docs requirements