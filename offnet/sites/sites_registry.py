from typing import List
import importlib

class SitesRegistry:
    def __init__(self):
        self.supported_sites = {
            'wikipedia': 'offnet.sites.wikipedia',
            'news': 'offnet.sites.wikipedia',  # Используем ту же логику
            'reddit': 'offnet.sites.wikipedia',
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
