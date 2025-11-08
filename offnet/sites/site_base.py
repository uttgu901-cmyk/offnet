from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseSite(ABC):
    """Base class for all site handlers"""
    
    @staticmethod
    @abstractmethod
    def search(content: dict, query: str, max_results: int = 5) -> List[dict]:
        pass
    
    @staticmethod
    @abstractmethod
    def get_article(content: dict, title: str) -> Optional[str]:
        pass
    
    @staticmethod
    def validate_content(content: dict) -> bool:
        """Validate content structure"""
        required = ['metadata', 'content']
        return all(field in content for field in required)
    
    @staticmethod
    def list_categories(content: dict) -> List[str]:
        """List available categories"""
        return content.get('metadata', {}).get('categories', [])
    
    @staticmethod
    def get_trending(content: dict) -> List[dict]:
        """Get trending content"""
        return content.get('metadata', {}).get('trending', [])
