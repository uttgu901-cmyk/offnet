import os
import json
import pickle
import hashlib
from typing import Dict, Optional
from datetime import datetime

class LocalStorage:
    """Manages local storage of site content"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.expanduser("~/.offnet")
        self.cache_dir = os.path.join(self.base_path, "cache")
        self.metadata_dir = os.path.join(self.base_path, "metadata")
        
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def save_site_content(self, site_name: str, content: dict):
        """Save site content to local cache"""
        cache_file = os.path.join(self.cache_dir, f"{site_name}.json")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    
    def load_site_content(self, site_name: str) -> Optional[dict]:
        """Load site content from local cache"""
        cache_file = os.path.join(self.cache_dir, f"{site_name}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def update_last_update(self, site_name: str):
        """Update last update timestamp"""
        import time
        metadata_file = os.path.join(self.metadata_dir, f"{site_name}.json")
        
        metadata = {
            'last_update': time.time(),
            'last_update_human': datetime.now().isoformat()
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def get_last_update(self, site_name: str) -> Optional[float]:
        """Get last update timestamp"""
        metadata_file = os.path.join(self.metadata_dir, f"{site_name}.json")
        
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    return metadata.get('last_update')
            except:
                return None
        return None
