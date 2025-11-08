import os
import json
from datetime import datetime

class LocalStorage:
    def __init__(self, base_path: str = "~/.offnet"):
        self.base_path = os.path.expanduser(base_path)
        self.cache_dir = os.path.join(self.base_path, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def save_site_content(self, site_name: str, content: dict):
        cache_file = os.path.join(self.cache_dir, f"{site_name}.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    
    def load_site_content(self, site_name: str):
        cache_file = os.path.join(self.cache_dir, f"{site_name}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
