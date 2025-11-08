from offnet.chat.gloff_chat import GloffChat

def chat(username="User"):
    return GloffChat(username)

def cite(site_name):
    class SiteHandler:
        def search(self, query):
            return [{"title": "Demo", "summary": "Test content"}]
    return SiteHandler()

def tool(tool_name):
    class Calculator:
        def calculate(self, expr):
            return eval(expr)
    return Calculator()

__all__ = ['chat', 'cite', 'tool', 'GloffChat']
