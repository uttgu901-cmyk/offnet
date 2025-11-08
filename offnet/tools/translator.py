class Translator:
    def __init__(self):
        self.dicts = {
            'en-es': {'hello': 'hola', 'goodbye': 'adiós', 'thank you': 'gracias'},
            'en-fr': {'hello': 'bonjour', 'goodbye': 'au revoir', 'thank you': 'merci'},
        }
    
    def translate(self, text: str, from_lang: str = 'en', to_lang: str = 'es'):
        key = f"{from_lang}-{to_lang}"
        dictionary = self.dicts.get(key, {})
        return ' '.join(dictionary.get(word.lower(), word) for word in text.split())
