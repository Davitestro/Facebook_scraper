"""
Improved Selenium-based Facebook Scraper with Infinite Scroll & Manual CAPTCHA
"""
from typing import Dict, Any, List, Optional, Set
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
import re
from urllib.parse import urlparse
from tqdm import tqdm

from .base_scraper import BaseScraper
from src.utils.rate_limiter import RateLimiter


class SeleniumScraper(BaseScraper):
    """Improved Facebook scraper with infinite scroll and CAPTCHA handling"""
    
    def __init__(self, headless: bool = False, config: Optional[Dict] = None):
        super().__init__(config)
        self.driver = None
        self.wait = None
        self.rate_limiter = RateLimiter(min_delay=1.0)
        self.seen_posts: Set[str] = set()
        self._setup_driver(headless)
        self.last_height = 0
        self.no_new_posts_count = 0
        
    def _setup_driver(self, headless: bool):
        """Setup Chrome WebDriver with anti-detection"""
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        # Anti-detection arguments
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Realistic user agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        
        # Additional options
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
        # Remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def _check_for_captcha(self) -> bool:
        """Check if CAPTCHA is present on the page"""
        captcha_indicators = [
            'div[aria-label="CAPTCHA"]',
            'img[alt*="captcha" i]',
            'img[alt*="验证码" i]',
            'div[role="dialog"]',
            'iframe[src*="captcha" i]',
            'iframe[src*="recaptcha" i]',
            'iframe[src*="hcaptcha" i]',
            'div[data-testid="captcha"]'
        ]
        
        for selector in captcha_indicators:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        return True
            except:
                continue
        
        # Check for text indicators
        page_text = self.driver.page_source.lower()
        captcha_keywords = ['captcha', '验证码', 'security check', 'verify', '确认']
        for keyword in captcha_keywords:
            if keyword in page_text:
                return True
        
        return False
    
    def login(self, email: str, password: str) -> bool:
        """Login to Facebook with manual CAPTCHA handling"""
        try:
            # Use non-headless for CAPTCHA handling
            self._setup_driver(headless=False)
            
            self.logger.info("🌐 Opening Facebook login page...")
            self.driver.get('https://www.facebook.com/login')
            time.sleep(5)
            
            # Check if already logged in
            if 'login' not in self.driver.current_url:
                self.logger.info("✅ Already logged in!")
                return True
            
            # Fill credentials
            try:
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'email'))
                )
                email_field.clear()
                email_field.send_keys(email)
                
                password_field = self.driver.find_element(By.ID, 'pass')
                password_field.clear()
                password_field.send_keys(password)
                
                login_button = self.driver.find_element(By.NAME, 'login')
                login_button.click()
                
            except Exception as e:
                self.logger.error(f"Error filling credentials: {e}")
                return False
            
            # Check for CAPTCHA
            if self._check_for_captcha():
                self.logger.info("🔐 CAPTCHA detected!")
                self.logger.info("👀 Please solve the CAPTCHA in the browser window...")
                self.logger.info("⏱️ You have 180 seconds to complete it")
                
                # Wait for CAPTCHA to be solved
                start_time = time.time()
                timeout = 180
                
                while time.time() - start_time < timeout:
                    # Check if CAPTCHA is gone
                    if not self._check_for_captcha():
                        # Check if login was successful
                        if 'login' not in self.driver.current_url:
                            self.logger.info("✅ CAPTCHA solved and login successful!")
                            return True
                    
                    # Check if user manually completed login
                    if 'login' not in self.driver.current_url:
                        self.logger.info("✅ Login completed manually!")
                        return True
                    
                    # Show progress every 10 seconds
                    elapsed = int(time.time() - start_time)
                    if elapsed % 10 == 0 and elapsed > 0:
                        self.logger.info(f"⏳ Waiting for CAPTCHA... ({elapsed}s elapsed)")
                    
                    time.sleep(2)
                
                self.logger.warning("⏰ Timeout waiting for CAPTCHA")
                return False
            
            # Check if login was successful
            if 'login' not in self.driver.current_url:
                self.logger.info("✅ Login successful!")
                return True
            
            self.logger.warning("⚠️ Login failed - check credentials")
            return False
            
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            try:
                self.driver.save_screenshot('login_error.png')
                self.logger.info("Screenshot saved as login_error.png")
            except:
                pass
            return False
    
    def _handle_login_overlay(self):
        """Handle Facebook login overlay if it appears"""
        try:
            # Check for login overlay
            overlay_selectors = [
                'div[role="dialog"]',
                'div[data-testid="cookie-policy"]',
                'div[aria-label="Close"]',
                'div[role="button"][aria-label*="close"]',
                'div[aria-label*="Close" i]'
            ]
            
            for selector in overlay_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            # Try to close it
                            try:
                                close_btn = element.find_element(By.CSS_SELECTOR, 'div[role="button"]')
                                close_btn.click()
                                time.sleep(1)
                                self.logger.info("Closed login overlay")
                            except:
                                pass
                except:
                    pass
            
            # Scroll to dismiss any remaining overlays
            self.driver.execute_script("window.scrollTo(0, 100);")
            time.sleep(1)
            
        except Exception as e:
            self.logger.debug(f"Error handling overlay: {e}")
    
    def scrape(self, url: str, **kwargs) -> Dict[str, Any]:
        """Scrape Facebook content with infinite scroll"""
        if not self._validate_url(url):
            raise ValueError(f"Invalid Facebook URL: {url}")
        
        max_posts = kwargs.get('max_posts', 50)
        scroll_pause = kwargs.get('scroll_pause', 2.0)
        max_scrolls = kwargs.get('max_scrolls', 100)
        
        self.seen_posts.clear()
        self.no_new_posts_count = 0
        
        try:
            self.driver.get(url)
            time.sleep(5)
            
            # Handle any login overlays
            self._handle_login_overlay()
            
            # Wait for page to load
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]'))
                )
            except:
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )
            
            # Determine page type
            if 'profile' in url or 'profile.php' in url:
                return self._scrape_profile(url)
            else:
                return self._scrape_page_with_scroll(url, max_posts, scroll_pause, max_scrolls)
                
        except Exception as e:
            self._handle_error(e, f"Scraping {url} failed")
            return {}
    
    def _scrape_page_with_scroll(self, url: str, max_posts: int, scroll_pause: float, max_scrolls: int) -> Dict[str, Any]:
        """Scrape page posts with infinite scroll until target reached"""
        posts = []
        scroll_attempts = 0
        
        # Initialize progress bar
        pbar = tqdm(
            total=max_posts,
            desc="Scraping posts",
            unit="posts",
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )
        
        self.logger.info(f"🎯 Target: {max_posts} posts. Starting infinite scroll...")
        
        while len(posts) < max_posts and scroll_attempts < max_scrolls:
            # Get current posts
            post_elements = self.driver.find_elements(
                By.CSS_SELECTOR, 'div[role="article"]'
            )
            
            new_posts_found = 0
            
            # Parse new posts
            for element in post_elements:
                if len(posts) >= max_posts:
                    break
                
                try:
                    post_data = self._extract_post_data(element)
                    post_id = post_data.get('post_id', '')
                    
                    if post_id and post_id not in self.seen_posts:
                        self.seen_posts.add(post_id)
                        posts.append(post_data)
                        new_posts_found += 1
                        pbar.update(1)
                        
                except Exception as e:
                    self.logger.debug(f"Error parsing post: {e}")
                    continue
            
            # Check if we reached target
            if len(posts) >= max_posts:
                self.logger.info(f"✅ Reached target of {max_posts} posts!")
                break
            
            # Check if no new posts found
            if new_posts_found == 0:
                self.no_new_posts_count += 1
                if self.no_new_posts_count >= 5:
                    self.logger.info(f"📭 No new posts found after {self.no_new_posts_count} scrolls. Reached end of page.")
                    break
            else:
                self.no_new_posts_count = 0
            
            # Check if we've reached the bottom
            current_height = self.driver.execute_script("return document.body.scrollHeight")
            if current_height == self.last_height and new_posts_found == 0:
                self.logger.info("📭 Reached bottom of page (no more content to load)")
                break
            
            # Smooth scroll with random behavior
            scroll_amount = min(500 + (scroll_attempts * 50), 1000)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Random pause to simulate human behavior
            time.sleep(scroll_pause + (scroll_attempts % 3) * 0.1)
            
            # Occasionally scroll back up a bit to trigger more loading
            if scroll_attempts % 3 == 0 and scroll_attempts > 0:
                self.driver.execute_script("window.scrollBy(0, -200);")
                time.sleep(0.5)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount + 100});")
            
            self.last_height = current_height
            scroll_attempts += 1
            
            # Update progress bar description with current count
            pbar.set_description(f"Scraping ({len(posts)} found)")
        
        pbar.close()
        
        # Final status
        if len(posts) >= max_posts:
            self.logger.info(f"✅ Successfully scraped {len(posts)} posts (target reached)")
        else:
            self.logger.info(f"📭 Scraping complete: found {len(posts)} posts (page ended)")
        
        return {
            'url': url,
            'posts': posts,
            'total_found': len(posts),
            'type': 'page',
            'page_title': self.driver.title if self.driver.title else '',
            'scroll_attempts': scroll_attempts,
            'target_reached': len(posts) >= max_posts
        }
    
    def _extract_post_data(self, element) -> Dict[str, Any]:
        """Extract comprehensive post data"""
        try:
            # Get post ID
            post_id = element.get_attribute('data-ft') or ''
            post_id_match = re.search(r'"top_level_post_id":"(\d+)"', post_id)
            post_id = post_id_match.group(1) if post_id_match else str(hash(str(element.text)))[:10]
            
            # Extract post text
            text = ''
            text_selectors = [
                'div[data-ad-preview="message"]',
                'div[data-testid="post_message"]',
                'div[dir="auto"] span',
                'div.x1lliihq span',
                'span[data-offset-key]'
            ]
            
            for selector in text_selectors:
                try:
                    text_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    if text_elements:
                        text = ' '.join([el.text for el in text_elements if el.text])
                        if text:
                            break
                except:
                    continue
            
            if not text:
                text = element.text.split('See more')[0].strip()
            
            # Extract author
            author = ''
            author_selectors = [
                'a[role="link"] span',
                'span.x1iorvi4 span',
                'h2 span span'
            ]
            for selector in author_selectors:
                try:
                    author_el = element.find_element(By.CSS_SELECTOR, selector)
                    if author_el:
                        author = author_el.text
                        break
                except:
                    continue
            
            # Extract timestamp
            timestamp = ''
            try:
                time_element = element.find_element(By.TAG_NAME, 'time')
                timestamp = time_element.get_attribute('datetime') or time_element.text
            except:
                timestamp = datetime.now().isoformat()
            
            # Extract link
            link = ''
            try:
                link_element = element.find_element(By.CSS_SELECTOR, 'a[role="link"]')
                link = link_element.get_attribute('href')
            except:
                link = ''
            
            # Extract engagement metrics
            likes = self._extract_engagement(element, 'like')
            comments = self._extract_engagement(element, 'comment')
            shares = self._extract_engagement(element, 'share')
            
            # Extract images
            images = []
            try:
                img_elements = element.find_elements(By.CSS_SELECTOR, 'img[src*=".jpg"], img[src*=".png"]')
                for img in img_elements[:5]:
                    src = img.get_attribute('src')
                    if src and 'static' not in src and 'scontent' in src:
                        images.append(src)
            except:
                pass
            
            # Extract video info
            has_video = False
            try:
                video_elements = element.find_elements(By.TAG_NAME, 'video')
                if video_elements:
                    has_video = True
            except:
                pass
            
            return {
                'post_id': post_id,
                'author': author or 'Unknown',
                'text': text,
                'full_text': text,
                'publish_date': timestamp,
                'timestamp_iso': self._convert_to_iso(timestamp),
                'link': link,
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'images': images,
                'has_video': has_video,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.debug(f"Error extracting post data: {e}")
            return {}
    
    def _extract_engagement(self, element, action_type):
        """Extract likes, comments, shares"""
        try:
            buttons = element.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
            
            for button in buttons:
                try:
                    aria_label = button.get_attribute('aria-label') or ''
                    text = button.text
                    
                    if action_type in aria_label.lower() or action_type in text.lower():
                        numbers = re.findall(r'\d+[\.,]?\d*', text)
                        if numbers:
                            num = numbers[0].replace(',', '').replace('.', '')
                            return int(float(num))
                        
                        count_match = re.search(r'(\d+[\.,]?\d*)', aria_label)
                        if count_match:
                            num = count_match.group(1).replace(',', '').replace('.', '')
                            return int(float(num))
                            
                        return 0
                except:
                    continue
            
            return 0
        except:
            return 0
    
    def _convert_to_iso(self, timestamp: str) -> str:
        """Convert Facebook timestamp to ISO format"""
        if not timestamp:
            return datetime.now().isoformat()
        
        try:
            if 'T' in timestamp:
                return timestamp
            
            current_time = datetime.now()
            
            if 'm' in timestamp and timestamp.endswith('m'):
                minutes = int(timestamp.replace('m', ''))
                dt = current_time - timedelta(minutes=minutes)
                return dt.isoformat()
            elif 'h' in timestamp and timestamp.endswith('h'):
                hours = int(timestamp.replace('h', ''))
                dt = current_time - timedelta(hours=hours)
                return dt.isoformat()
            elif 'd' in timestamp and timestamp.endswith('d'):
                days = int(timestamp.replace('d', ''))
                dt = current_time - timedelta(days=days)
                return dt.isoformat()
            elif 'w' in timestamp and timestamp.endswith('w'):
                weeks = int(timestamp.replace('w', ''))
                dt = current_time - timedelta(weeks=weeks)
                return dt.isoformat()
            elif 'y' in timestamp and timestamp.endswith('y'):
                years = int(timestamp.replace('y', ''))
                dt = current_time - timedelta(days=years*365)
                return dt.isoformat()
            else:
                return timestamp
        except:
            return timestamp
    
    def _scrape_profile(self, url: str) -> Dict[str, Any]:
        """Scrape user profile with more details"""
        try:
            profile_data = {
                'url': url,
                'type': 'profile'
            }
            
            try:
                name_selectors = ['h1', 'h2', 'div[data-testid="profile_name"]']
                for selector in name_selectors:
                    try:
                        name_el = self.driver.find_element(By.CSS_SELECTOR, selector)
                        profile_data['name'] = name_el.text
                        break
                    except:
                        continue
            except:
                profile_data['name'] = 'Unknown'
            
            try:
                bio = self.driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="profile_description"]'
                ).text
                profile_data['bio'] = bio
            except:
                profile_data['bio'] = ''
            
            try:
                img = self.driver.find_element(By.CSS_SELECTOR, 'img[alt*="profile"]')
                profile_data['profile_picture'] = img.get_attribute('src')
            except:
                profile_data['profile_picture'] = ''
            
            try:
                followers = self.driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="follower_count"]'
                ).text
                profile_data['followers'] = followers
            except:
                profile_data['followers'] = '0'
            
            return profile_data
            
        except Exception as e:
            self.logger.error(f"Profile scraping failed: {e}")
            return {'url': url, 'type': 'profile', 'error': str(e)}
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()