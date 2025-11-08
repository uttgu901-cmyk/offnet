from .site_base import BaseSite
from typing import Dict, List, Optional

class WikipediaSite(BaseSite):
    
    @staticmethod
    def search(content: dict, query: str, max_results: int = 5) -> List[dict]:
        results = []
        query_lower = query.lower()
        
        articles = content.get('content', {}).get('articles', {})
        
        for title, article_data in articles.items():
            content_text = article_data.get('content', '').lower()
            summary = article_data.get('summary', '')
            
            if (query_lower in title.lower() or 
                query_lower in content_text or
                query_lower in summary.lower()):
                
                results.append({
                    'title': title,
                    'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                    'url': f"https://wikipedia.org/wiki/{title.replace(' ', '_')}",
                    'category': article_data.get('category', 'General')
                })
            
            if len(results) >= max_results:
                break
        
        return results
    
    @staticmethod
    def get_article(content: dict, title: str) -> Optional[str]:
        articles = content.get('content', {}).get('articles', {})
        article_data = articles.get(title)
        if article_data:
            return article_data.get('content', 'Article content not available')
        return None
    
    @staticmethod
    def validate_content(content: dict) -> bool:
        if not super().validate_content(content):
            return False
        
        articles = content.get('content', {}).get('articles', {})
        return len(articles) > 0
