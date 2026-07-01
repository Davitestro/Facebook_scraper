"""
Configuration Management
"""
import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Facebook Credentials
    FACEBOOK_EMAIL: str = os.getenv('FACEBOOK_EMAIL', '')
    FACEBOOK_PASSWORD: str = os.getenv('FACEBOOK_PASSWORD', '')
    ACCESS_TOKEN: str = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    
    # Scraping Settings
    MAX_RETRIES: int = 3
    REQUEST_DELAY: float = 2.0
    MAX_POSTS: int = 100
    TIMEOUT: int = 30
    
    # Browser Settings
    HEADLESS: bool = False
    USER_AGENT: str = os.getenv('USER_AGENT', 'Mozilla/5.0...')
    
    # Storage Settings
    DATA_DIR: str = 'data/'
    LOG_DIR: str = 'logs/'
    
    # Proxy Settings (optional)
    USE_PROXY: bool = False
    PROXY_LIST: list[str] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, yaml_path: str):
        """Load config from YAML file"""
        import yaml
        with open(yaml_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)