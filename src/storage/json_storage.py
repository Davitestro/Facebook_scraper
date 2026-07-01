"""
JSON Storage Handler
"""
import json
import os
from typing import Any, Dict, List
from datetime import datetime

class JSONStorage:
    """Handle JSON file storage"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_directory()
        
    def _ensure_directory(self):
        """Create directory if it doesn't exist"""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save(self, data: Dict[str, Any]):
        """Save data to JSON file"""
        # Add metadata
        output_data = {
            'metadata': {
                'scraped_at': datetime.now().isoformat(),
                'total_items': len(data.get('posts', []))
            },
            'data': data
        }
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    def load(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
            
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def append(self, new_data: Dict[str, Any]):
        """Append to existing JSON file"""
        current_data = self.load() if os.path.exists(self.filepath) else {}
        current_data.update(new_data)
        self.save(current_data)