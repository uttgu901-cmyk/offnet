from typing import Dict, List
import importlib

class SitesRegistry:
    """Registry of supported sites"""
    
    def __init__(self):
        self.supported_sites = {
            # Knowledge
            'wikipedia': 'offnet.sites.wikipedia',
            'stackoverflow': 'offnet.sites.stackoverflow',
            'github': 'offnet.sites.github',
            'docs-python': 'offnet.sites.docs_python',
            
            # News & Media
            'reddit': 'offnet.sites.reddit', 
            'medium': 'offnet.sites.medium',
            'hackernews': 'offnet.sites.hackernews',
            'bbc-news': 'offnet.sites.bbc_news',
            
            # Documentation
            'mdn-web-docs': 'offnet.sites.mdn_web_docs',
            'w3schools': 'offnet.sites.w3schools',
            'devdocs': 'offnet.sites.devdocs',
            
            # Programming
            'realpython': 'offnet.sites.realpython',
            'python-org': 'offnet.sites.python_org',
            'stackexchange': 'offnet.sites.stackexchange',
            
            # Add more popular sites here...
        }
    
    def is_supported(self, site_name: str) -> bool:
        return site_name in self.supported_sites
    
    def list_sites(self) -> List[str]:
        return list(self.supported_sites.keys())
    
    def get_site_module(self, site_name: str):
        if not self.is_supported(site_name):
            raise ValueError(f"Site '{site_name}' not supported")
        
        module_path = self.supported_sites[site_name]
        return importlib.import_module(module_path)
