import os
import json
import requests
import hashlib
from typing import Dict, List, Optional
import click
from .sites.sites_registry import SitesRegistry
from .utils.storage import LocalStorage
from .tools.calculator import Calculator
from .tools.translator import Translator
from .tools.weather import Weather
from .tools.notes import Notes

class OffWorld:
    """
    Main class for OffNet library - provides offline access to web content
    """
    
    def __init__(self):
        self.sites_registry = SitesRegistry()
        self.storage = LocalStorage()
        self.gh_raw_url = "https://raw.githubusercontent.com/yourusername/offnet-data/main"
        self._tools = {}
        self._init_tools()
        
    def _init_tools(self):
        """Initialize offline tools"""
        self._tools = {
            'calculator': Calculator(),
            'translator': Translator(), 
            'weather': Weather(),
            'notes': Notes()
        }
    
    def cite(self, site_name: str) -> 'SiteHandler':
        """Register a site for offline access"""
        if not self.sites_registry.is_supported(site_name):
            available = self.sites_registry.list_sites()
            raise ValueError(f"Site '{site_name}' is not supported. Available sites: {available}")
        
        return SiteHandler(site_name, self)
    
    def get_tool(self, tool_name: str):
        """Get an offline tool"""
        tool = self._tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found. Available: {list(self._tools.keys())}")
        return tool
    
    def update_content(self, site_name: str, force: bool = False) -> bool:
        """Update local content from GitHub repository"""
        if not self.sites_registry.is_supported(site_name):
            raise ValueError(f"Site {site_name} not supported")
        
        # Check if update is needed
        if not force and not self._should_update(site_name):
            return True
            
        try:
            # Fetch content from GitHub
            content_url = f"{self.gh_raw_url}/sites/{site_name}/content.json"
            response = requests.get(content_url, timeout=30)
            
            if response.status_code == 200:
                content = response.json()
                
                # Validate content structure
                if self._validate_content(site_name, content):
                    self.storage.save_site_content(site_name, content)
                    self.storage.update_last_update(site_name)
                    print(f"✓ Updated {site_name}")
                    return True
                else:
                    print(f"✗ Invalid content structure for {site_name}")
                    return False
            else:
                print(f"✗ Could not fetch {site_name}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error updating {site_name}: {e}")
            return False
    
    def _should_update(self, site_name: str) -> bool:
        """Check if content should be updated"""
        last_update = self.storage.get_last_update(site_name)
        if not last_update:
            return True
            
        import time
        # Update if older than 7 days
        return time.time() - last_update > 7 * 24 * 60 * 60
    
    def _validate_content(self, site_name: str, content: dict) -> bool:
        """Validate content structure"""
        required_fields = ['metadata', 'content']
        if not all(field in content for field in required_fields):
            return False
        
        site_module = self.sites_registry.get_site_module(site_name)
        return site_module.validate_content(content)

class SiteHandler:
    """Handler for specific site operations"""
    
    def __init__(self, site_name: str, offworld: OffWorld):
        self.site_name = site_name
        self.offworld = offworld
        self.site_module = offworld.sites_registry.get_site_module(site_name)
        self.content = self._load_content()
    
    def _load_content(self) -> dict:
        """Load content from local storage"""
        content = self.offworld.storage.load_site_content(self.site_name)
        if not content:
            raise ConnectionError(f"Could not load content for {self.site_name}. Run 'offnet-update' first.")
        return content
    
    def search(self, query: str, max_results: int = 5) -> List[dict]:
        """Search within the site content"""
        return self.site_module.search(self.content, query, max_results)
    
    def get_article(self, title: str) -> Optional[str]:
        """Get specific article by title"""
        return self.site_module.get_article(self.content, title)
    
    def list_categories(self) -> List[str]:
        """List available categories"""
        return self.site_module.list_categories(self.content)
    
    def get_trending(self) -> List[dict]:
        """Get trending content"""
        return self.site_module.get_trending(self.content)

def update_all_content():
    """Update all site content"""
    offworld = OffWorld()
    sites = offworld.sites_registry.list_sites()
    
    print("Updating all site content...")
    for site in sites:
        offworld.update_content(site, force=True)

def update_all_content_cli():
    """CLI entry point for updating content"""
    update_all_content()
