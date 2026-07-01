"""
Facebook Scraper - Main Entry Point
"""
import argparse
import logging
from src.config import Config
from src.scrapers.selenium_scraper import SeleniumScraper
from src.scrapers.api_scraper import APIScraper
from src.storage.json_storage import JSONStorage
from src.utils.logger import setup_logger

def main():
    parser = argparse.ArgumentParser(description='Facebook Scraper')
    parser.add_argument('--method', choices=['selenium', 'api'], default='selenium',
                       help='Scraping method to use')
    parser.add_argument('--url', help='Facebook URL to scrape')
    parser.add_argument('--output', default='data/raw/output.json',
                       help='Output file path')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger()
    
    try:
        # Initialize scraper
        if args.method == 'selenium':
            scraper = SeleniumScraper(headless=args.headless)
        else:
            scraper = APIScraper(Config.ACCESS_TOKEN)
        
        # Scrape data
        logger.info(f"Starting scrape with {args.method}")
        data = scraper.scrape(args.url)
        
        # Save data
        storage = JSONStorage(args.output)
        storage.save(data)
        
        logger.info(f"Data saved to {args.output}")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise
    finally:
        if 'scraper' in locals():
            scraper.close()

if __name__ == '__main__':
    main()