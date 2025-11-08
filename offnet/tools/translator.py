class Translator:
    """Offline translator using pre-loaded dictionaries"""
    
    def __init__(self):
        self.dictionaries = {
            'en-es': self._load_en_es(),
            'en-fr': self._load_en_fr(),
            'en-de': self._load_en_de(),
            # Add more languages as needed
        }
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
        """Translate text between languages"""
        dict_key = f"{source_lang}-{target_lang}"
        
        if dict_key not in self.dictionaries:
            raise ValueError(f"Translation from {source_lang} to {target_lang} not supported")
        
        dictionary = self.dictionaries[dict_key]
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            # Remove punctuation for matching
            clean_word = ''.join(c for c in word if c.isalnum())
            translated = dictionary.get(clean_word, word)
            translated_words.append(translated)
        
        return ' '.join(translated_words)
    
    def _load_en_es(self) -> dict:
        """English to Spanish dictionary"""
        return {
            'hello': 'hola',
            'goodbye': 'adiós',
            'please': 'por favor',
            'thank': 'gracias',
            'yes': 'sí',
            'no': 'no',
            'water': 'agua',
            'food': 'comida',
            'help': 'ayuda',
            'time': 'tiempo',
            'day': 'día',
            'night': 'noche',
            'house': 'casa',
            'car': 'coche',
            'book': 'libro',
            'computer': 'computadora',
            'phone': 'teléfono',
            'friend': 'amigo',
            'family': 'familia',
            'work': 'trabajo',
            'school': 'escuela',
            'city': 'ciudad',
            'country': 'país',
        }
    
    def _load_en_fr(self) -> dict:
        """English to French dictionary"""
        return {
            'hello': 'bonjour',
            'goodbye': 'au revoir',
            'please': 's il vous plaît',
            'thank': 'merci',
            'yes': 'oui',
            'no': 'non',
            'water': 'eau',
            'food': 'nourriture',
            'help': 'aide',
            'time': 'temps',
            'day': 'jour',
            'night': 'nuit',
            'house': 'maison',
            'car': 'voiture',
            'book': 'livre',
            'computer': 'ordinateur',
            'phone': 'téléphone',
            'friend': 'ami',
            'family': 'famille',
            'work': 'travail',
            'school': 'école',
            'city': 'ville',
            'country': 'pays',
        }
    
    def _load_en_de(self) -> dict:
        """English to German dictionary"""
        return {
            'hello': 'hallo',
            'goodbye': 'auf wiedersehen',
            'please': 'bitte',
            'thank': 'danke',
            'yes': 'ja',
            'no': 'nein',
            'water': 'wasser',
            'food': 'lebensmittel',
            'help': 'hilfe',
            'time': 'zeit',
            'day': 'tag',
            'night': 'nacht',
            'house': 'haus',
            'car': 'auto',
            'book': 'buch',
            'computer': 'computer',
            'phone': 'telefon',
            'friend': 'freund',
            'family': 'familie',
            'work': 'arbeit',
            'school': 'schule',
            'city': 'stadt',
            'country': 'land',
        }
