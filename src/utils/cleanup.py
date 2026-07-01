"""
Data cleanup utilities
"""
import re  # Add this import
from typing import List, Dict, Any
from datetime import datetime
import json

def deduplicate_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate posts based on post_id"""
    seen = set()
    unique_posts = []
    
    for post in posts:
        post_id = post.get('post_id', '')
        if post_id and post_id not in seen:
            seen.add(post_id)
            unique_posts.append(post)
        elif not post_id:
            # If no ID, use text + timestamp hash
            key = f"{post.get('text', '')}_{post.get('timestamp', '')}"
            if key not in seen:
                seen.add(key)
                unique_posts.append(post)
    
    return unique_posts

def enrich_post_data(post: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich post data with additional fields"""
    post['scraped_at'] = datetime.now().isoformat()
    post['word_count'] = len(post.get('text', '').split())
    post['char_count'] = len(post.get('text', ''))
    
    # Extract hashtags
    hashtags = re.findall(r'#\w+', post.get('text', ''))
    post['hashtags'] = hashtags
    
    # Extract mentions
    mentions = re.findall(r'@\w+', post.get('text', ''))
    post['mentions'] = mentions
    
    return post