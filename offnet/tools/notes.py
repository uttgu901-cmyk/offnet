import os
import json
from datetime import datetime

class Notes:
    def __init__(self):
        self.notes_dir = "~/.offnet/notes"
        os.makedirs(os.path.expanduser(self.notes_dir), exist_ok=True)
    
    def create_note(self, title: str, content: str):
        note_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        note_file = os.path.join(os.path.expanduser(self.notes_dir), f"{note_id}.json")
        
        with open(note_file, 'w') as f:
            json.dump({'title': title, 'content': content, 'id': note_id}, f)
        
        return note_id
