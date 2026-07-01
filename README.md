# Facebook Scraper
## A comprehensive Facebook scraper built with Python and Selenium.

# Features

### Profile Scraping: Extract user profiles, bios, and public details.

### Post Scraping: Collect post text, timestamps, and engagement metrics.

### Comment Extraction: Parse multi-level comment threads from targeted posts.

### Flexible Data Storage: Export data seamlessly into multiple formats (JSON, CSV).

### Anti-Bot Mitigation: Built-in rate limiting and robust proxy rotation support.

### Containerized Deployment: Ready-to-go Docker configuration for isolated execution.

Installation
Bash
# Clone repository
gh repo clone Davitestro/Facebook_scraper
cd facebook-scraper

# Install dependencies
pip install -r requirements/base.txt

# Copy environment file
cp .env.example .env
# Edit .env with your credentials
Usage
Basic Execution
Bash
python -m src.main --url https://www.facebook.com/facebook
Advanced Execution
Bash
python -m src.main --method selenium --url https://www.facebook.com/facebook --output data/export.json --headless
Docker Execution
Bash
# Build the Docker image
docker-compose build

# Run the scraper container
docker-compose run --rm scraper python -m src.main --url https://www.facebook.com/facebook
Project Structure Setup
To mirror the recommended architecture for this project, you can generate the entire directory structure automatically using the following commands:

Bash
# Create root directory and navigate inside
mkdir facebook-scraper
cd facebook-scraper

# Generate core application and testing modules
mkdir -p src/{scrapers,parsers,storage,utils,exceptions}
mkdir -p tests/{test_scrapers,test_parsers,test_utils}

# Generate data reservoirs and configuration assets
mkdir -p data/{raw,processed,exports}
mkdir -p logs config scripts docs requirements