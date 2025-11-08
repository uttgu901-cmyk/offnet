import os
import json
from typing import List
from .sites.sites_registry import SitesRegistry
from .utils.storage import LocalStorage
from .tools.calculator import Calculator
from .tools.translator import Translator
from .tools.weather import Weather
from .tools.notes import Notes

class OffWorld:
    def __init__(self):
        self.sites_registry = SitesRegistry()
        self.storage = LocalStorage()
        self._tools = {
            'calculator': Calculator(),
            'translator': Translator(),
            'weather': Weather(),
            'notes': Notes()
        }
        self._load_builtin_content()
    
    def _load_builtin_content(self):
        """Загружает встроенные данные из папки sites/"""
        for site_name in self.sites_registry.list_sites():
            content = self._load_local_content(site_name)
            if content:
                self.storage.save_site_content(site_name, content)
    
    def _load_local_content(self, site_name: str):
        """Загружает данные из локальной папки sites/"""
        try:
            content_path = f"sites/{site_name}/content.json"
            if os.path.exists(content_path):
                with open(content_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return None
    
    def cite(self, site_name: str):
        if not self.sites_registry.is_supported(site_name):
            available = self.sites_registry.list_sites()
            raise ValueError(f"Site '{site_name}' not supported. Available: {available}")
        
        return SiteHandler(site_name, self)
    
    def get_tool(self, tool_name: str):
        tool = self._tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found. Available: {list(self._tools.keys())}")
        return tool

class SiteHandler:
    def __init__(self, site_name: str, offworld: OffWorld):
        self.site_name = site_name
        self.offworld = offworld
        self.site_module = offworld.sites_registry.get_site_module(site_name)
        self.content = self._load_content()
    
    def _load_content(self):
        content = self.offworld.storage.load_site_content(self.site_name)
        if not content:
            raise ConnectionError(f"No content for {self.site_name}. Run 'offnet-update' first.")
        return content
    
    def search(self, query: str, max_results: int = 5):
        return self.site_module.search(self.content, query, max_results)
    
    def get_article(self, title: str):
        return self.site_module.get_article(self.content, title)

def update_all_content():
    """Обновляет все данные"""
    print("Updating content...")
    # В реальности здесь будет вызов скрипта парсера
    print("Run: python scripts/mass_parser.py")

def update_all_content_cli():
    update_all_content()
