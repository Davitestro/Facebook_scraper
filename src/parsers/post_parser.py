"""
Enhanced Post Parser
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class PostParser:
    """Parse Facebook post data with better extraction"""
    
    @staticmethod
    def parse(post_element) -> Dict[str, Any]:
        """Parse post element comprehensively"""
        try:
            # Extract post ID
            post_id = PostParser._extract_post_id(post_element)
            
            # Extract all data
            data = {
                'post_id': post_id,
                'author': PostParser._extract_author(post_element),
                'text': PostParser._extract_text(post_element),
                'timestamp': PostParser._extract_timestamp(post_element),
                'timestamp_iso': None,
                'link': PostParser._extract_link(post_element),
                'images': PostParser._extract_images(post_element),
                'video': PostParser._extract_video(post_element),
                'likes': PostParser._extract_likes(post_element),
                'comments': PostParser._extract_comments(post_element),
                'shares': PostParser._extract_shares(post_element),
                'scraped_at': datetime.now().isoformat()
            }
            
            # Convert timestamp to ISO
            if data['timestamp']:
                data['timestamp_iso'] = PostParser._convert_timestamp(data['timestamp'])
            
            return data
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _extract_post_id(element) -> str:
        """Extract unique post ID"""
        try:
            ft_data = element.get_attribute('data-ft')
            if ft_data:
                match = re.search(r'"top_level_post_id":"(\d+)"', ft_data)
                if match:
                    return match.group(1)
            
            # Fallback: hash of content
            return str(hash(element.text + str(datetime.now()))) 
        except:
            return str(hash(str(datetime.now())))
    
    @staticmethod
    def _extract_text(element) -> str:
        """Extract full post text"""
        text = ''
        
        # Try multiple selectors
        selectors = [
            'div[data-ad-preview="message"]',
            'div[data-testid="post_message"]',
            'div[dir="auto"] span',
            'span[data-offset-key]'
        ]
        
        for selector in selectors:
            try:
                elements = element.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    text = ' '.join([el.text for el in elements if el.text])
                    if text:
                        break
            except:
                continue
        
        # If still empty, try getting all text without "See more"
        if not text:
            full_text = element.text
            text = full_text.split('See more')[0].strip()
        
        return text
    
    @staticmethod
    def _extract_timestamp(element) -> str:
        """Extract and normalize timestamp"""
        try:
            time_elem = element.find_element(By.TAG_NAME, 'time')
            timestamp = time_elem.get_attribute('datetime')
            if not timestamp:
                timestamp = time_elem.text
            return timestamp
        except:
            return ''
    
    @staticmethod
    def _convert_timestamp(timestamp: str) -> str:
        """Convert Facebook timestamp to ISO format"""
        if not timestamp:
            return datetime.now().isoformat()
        
        try:
            # Already ISO
            if 'T' in timestamp and '-' in timestamp:
                return timestamp
            
            # Relative time conversion
            now = datetime.now()
            timestamp = timestamp.lower().strip()
            
            if 'minute' in timestamp or 'm' in timestamp:
                minutes = re.search(r'(\d+)', timestamp)
                if minutes:
                    dt = now - timedelta(minutes=int(minutes.group(1)))
                    return dt.isoformat()
            elif 'hour' in timestamp or 'h' in timestamp:
                hours = re.search(r'(\d+)', timestamp)
                if hours:
                    dt = now - timedelta(hours=int(hours.group(1)))
                    return dt.isoformat()
            elif 'day' in timestamp or 'd' in timestamp:
                days = re.search(r'(\d+)', timestamp)
                if days:
                    dt = now - timedelta(days=int(days.group(1)))
                    return dt.isoformat()
            elif 'week' in timestamp or 'w' in timestamp:
                weeks = re.search(r'(\d+)', timestamp)
                if weeks:
                    dt = now - timedelta(weeks=int(weeks.group(1)))
                    return dt.isoformat()
            elif 'month' in timestamp:
                months = re.search(r'(\d+)', timestamp)
                if months:
                    dt = now - timedelta(days=int(months.group(1))*30)
                    return dt.isoformat()
            elif 'year' in timestamp or 'y' in timestamp:
                years = re.search(r'(\d+)', timestamp)
                if years:
                    dt = now - timedelta(days=int(years.group(1))*365)
                    return dt.isoformat()
            else:
                # Try parsing as actual date
                try:
                    from dateutil import parser
                    dt = parser.parse(timestamp)
                    return dt.isoformat()
                except:
                    return timestamp
                    
            return timestamp
            
        except Exception as e:
            return timestamp
    
    @staticmethod
    def _extract_author(element) -> str:
        """Extract author name"""
        selectors = [
            'a[role="link"] span',
            'h3 span',
            'span.x1iorvi4 span'
        ]
        
        for selector in selectors:
            try:
                author_el = element.find_element(By.CSS_SELECTOR, selector)
                if author_el.text:
                    return author_el.text
            except:
                continue
        
        return ''
    
    @staticmethod
    def _extract_link(element) -> str:
        """Extract post link"""
        try:
            link_elem = element.find_element(By.CSS_SELECTOR, 'a[role="link"]')
            return link_elem.get_attribute('href')
        except:
            return ''
    
    @staticmethod
    def _extract_images(element) -> list:
        """Extract image URLs"""
        images = []
        try:
            img_elements = element.find_elements(
                By.CSS_SELECTOR, 'img[src*=".jpg"], img[src*=".png"]'
            )
            for img in img_elements[:5]:
                src = img.get_attribute('src')
                if src and 'static' not in src and 'scontent' in src:
                    images.append(src)
        except:
            pass
        return images
    
    @staticmethod
    def _extract_video(element) -> bool:
        """Check if post has video"""
        try:
            video_elements = element.find_elements(By.TAG_NAME, 'video')
            return len(video_elements) > 0
        except:
            return False
    
    @staticmethod
    def _extract_likes(element) -> int:
        """Extract like count"""
        return PostParser._extract_count(element, ['like', 'likes'])
    
    @staticmethod
    def _extract_comments(element) -> int:
        """Extract comment count"""
        return PostParser._extract_count(element, ['comment', 'comments'])
    
    @staticmethod
    def _extract_shares(element) -> int:
        """Extract share count"""
        return PostParser._extract_count(element, ['share', 'shares'])
    
    @staticmethod
    def _extract_count(element, keywords: list) -> int:
        """Generic count extractor"""
        try:
            # Get all text in element
            text = element.text
            
            # Find numbers near keywords
            for keyword in keywords:
                pattern = rf'(\d+[\.,]?\d*)\s*{keyword}'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    num = match.group(1).replace(',', '').replace('.', '')
                    return int(float(num))
            
            # Try aria-label approach
            buttons = element.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
            for button in buttons:
                aria_label = button.get_attribute('aria-label') or ''
                for keyword in keywords:
                    if keyword in aria_label.lower():
                        numbers = re.findall(r'\d+', aria_label)
                        if numbers:
                            return int(numbers[0])
            
            return 0
        except:
            return 0