"""
Facebook Scraper - Main Entry Point with improved output
"""
import argparse
import logging
import json
from datetime import datetime
from src.config import Config
from src.scrapers.selenium_scraper import SeleniumScraper
from src.storage.json_storage import JSONStorage
from src.utils.logger import setup_logger
from src.utils.cleanup import deduplicate_posts, enrich_post_data

def main():
    parser = argparse.ArgumentParser(description='Facebook Scraper')
    parser.add_argument('--method', choices=['selenium', 'api'], default='selenium',
                       help='Scraping method to use')
    parser.add_argument('--url', help='Facebook URL to scrape')
    parser.add_argument('--output', default='data/raw/output.json',
                       help='Output file path')
    parser.add_argument('--max-posts', type=int, default=50,
                       help='Maximum posts to scrape')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--no-login', action='store_true',  # Add this
                       help='Skip login (for public pages)')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger()
    
    try:
        # Initialize scraper
        scraper = SeleniumScraper(headless=args.headless)
        
        # Login only if credentials provided and not skipped
        if not args.no_login and Config.FACEBOOK_EMAIL and Config.FACEBOOK_PASSWORD:
            logger.info("Attempting to login...")
            login_success = scraper.login(Config.FACEBOOK_EMAIL, Config.FACEBOOK_PASSWORD)
            if not login_success:
                logger.warning("Login failed, continuing without login (may limit data)")
        else:
            logger.info("Skipping login (using --no-login or no credentials)")
        
        # Scrape data
        logger.info(f"Starting scrape with {args.method} from {args.url}")
        result = scraper.scrape(args.url, max_posts=args.max_posts)
        
        # Clean and deduplicate posts
        if 'posts' in result and result['posts']:
            original_count = len(result['posts'])
            result['posts'] = deduplicate_posts(result['posts'])
            result['posts'] = [enrich_post_data(post) for post in result['posts']]
            result['total_found'] = len(result['posts'])
            result['duplicates_removed'] = original_count - len(result['posts'])
        else:
            result['total_found'] = 0
            result['duplicates_removed'] = 0
        
        # Add metadata
        result['scraping_metadata'] = {
            'scraped_at': datetime.now().isoformat(),
            'method': args.method,
            'max_posts': args.max_posts,
            'url': args.url,
            'login_used': not args.no_login
        }
        
        # Save data
        storage = JSONStorage(args.output)
        storage.save(result)
        
        logger.info(f"Data saved to {args.output}")
        logger.info(f"Total posts: {result.get('total_found', 0)}")
        logger.info(f"Duplicates removed: {result.get('duplicates_removed', 0)}")
        
        # Print sample
        if result.get('posts'):
            sample = result['posts'][0]
            logger.info(f"Sample post: {sample.get('text', '')[:100]}...")
        else:
            logger.warning("No posts found! The page might require login or have no content.")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if 'scraper' in locals():
            scraper.close()

if __name__ == '__main__':
    main()