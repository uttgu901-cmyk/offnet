from typing import List

class BaseSite:
    @staticmethod
    def search(content: dict, query: str, max_results: int = 5):
        results = []
        query_lower = query.lower()
        
        articles = content.get('content', {}).get('articles', {})
        
        for title, article_data in articles.items():
            content_text = article_data.get('content', '').lower()
            if query_lower in title.lower() or query_lower in content_text:
                results.append({
                    'title': title,
                    'summary': article_data.get('summary', '')[:200] + '...',
                    'url': article_data.get('url', '')
                })
            
            if len(results) >= max_results:
                break
        
        return results
    
    @staticmethod
    def get_article(content: dict, title: str):
        articles = content.get('content', {}).get('articles', {})
        article_data = articles.get(title)
        if article_data:
            return article_data.get('content', 'Content not available')
        return None
