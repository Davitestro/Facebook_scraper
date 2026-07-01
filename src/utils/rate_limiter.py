"""
Rate Limiter Utility
"""
import time
from threading import Lock
from typing import Optional

class RateLimiter:
    """Simple rate limiter with exponential backoff"""
    
    def __init__(self, min_delay: float = 1.0, max_delay: float = 10.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0
        self.failure_count = 0
        self.lock = Lock()
        
    def wait(self):
        """Wait if needed to respect rate limits"""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            # Calculate delay with backoff
            delay = self.min_delay * (2 ** self.failure_count)
            delay = min(delay, self.max_delay)
            
            if time_since_last < delay:
                time.sleep(delay - time_since_last)
            
            self.last_request_time = time.time()
    
    def record_failure(self):
        """Record a failure to increase backoff"""
        with self.lock:
            self.failure_count = min(self.failure_count + 1, 5)
    
    def record_success(self):
        """Record a success to decrease backoff"""
        with self.lock:
            self.failure_count = max(self.failure_count - 1, 0)