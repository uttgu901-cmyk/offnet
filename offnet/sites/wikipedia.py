from .site_base import BaseSite

class WikipediaSite(BaseSite):
    # Используем базовую реализацию
    pass

# Для обратной совместимости
search = WikipediaSite.search
get_article = WikipediaSite.get_article
