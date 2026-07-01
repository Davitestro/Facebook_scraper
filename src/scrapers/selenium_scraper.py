"""
Selenium-based Facebook Scraper
"""
from typing import Dict, Any, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

from .base_scraper import BaseScraper
from src.parsers.post_parser import PostParser
from src.parsers.profile_parser import ProfileParser
from src.utils.rate_limiter import RateLimiter

class SeleniumScraper(BaseScraper):
    """Facebook scraper using Selenium WebDriver"""
    
    def __init__(self, headless: bool = False, config: Optional[Dict] = None):
        super().__init__(config)
        self.driver = None
        self.wait = None
        self.rate_limiter = RateLimiter(min_delay=2.0)
        self._setup_driver(headless)
        
    def _setup_driver(self, headless: bool):
        """Setup Chrome WebDriver"""
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent
        options.add_argument(f'user-agent={self.config.get("user_agent", "Mozilla/5.0...")}')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def login(self, email: str, password: str):
        """Login to Facebook"""
        self.driver.get('https://www.facebook.com/login')
        time.sleep(2)
        
        try:
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.ID, 'pass')
            password_field.send_keys(password)
            
            login_button = self.driver.find_element(By.NAME, 'login')
            login_button.click()
            
            time.sleep(5)
            return True
            
        except Exception as e:
            self._handle_error(e, "Login failed")
            return False
    
    def scrape(self, url: str, **kwargs) -> Dict[str, Any]:
        """Scrape Facebook content"""
        if not self._validate_url(url):
            raise ValueError(f"Invalid Facebook URL: {url}")
        
        self.rate_limiter.wait()
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # Determine what type of page we're scraping
            if 'profile' in url or 'profile.php' in url:
                return self._scrape_profile(url)
            else:
                return self._scrape_page(url, kwargs.get('max_posts', 50))
                
        except Exception as e:
            self._handle_error(e, f"Scraping {url} failed")
            return {}
    
    def _scrape_profile(self, url: str) -> Dict[str, Any]:
        """Scrape user profile"""
        parser = ProfileParser()
        
        try:
            # Extract profile info
            name = self.driver.find_element(By.CSS_SELECTOR, 'h1').text
            bio = self.driver.find_element(
                By.CSS_SELECTOR, 'div[data-testid="profile_description"]'
            ).text
            
            return {
                'url': url,
                'name': name,
                'bio': bio,
                'type': 'profile'
            }
            
        except Exception as e:
            self.logger.warning(f"Could not parse profile: {e}")
            return {'url': url, 'type': 'profile', 'error': str(e)}
    
    def _scrape_page(self, url: str, max_posts: int) -> Dict[str, Any]:
        """Scrape page posts"""
        posts = []
        parser = PostParser()
        scroll_attempts = 0
        
        while len(posts) < max_posts and scroll_attempts < 20:
            # Find posts
            post_elements = self.driver.find_elements(
                By.CSS_SELECTOR, 'div[role="article"]'
            )
            
            for element in post_elements:
                if len(posts) >= max_posts:
                    break
                    
                try:
                    post_data = parser.parse(element)
                    if post_data:
                        posts.append(post_data)
                except Exception as e:
                    self.logger.debug(f"Error parsing post: {e}")
                    continue
            
            # Scroll down
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)
            scroll_attempts += 1
            
        return {
            'url': url,
            'posts': posts,
            'total_found': len(posts),
            'type': 'page'
        }
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()