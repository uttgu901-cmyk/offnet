import os
import json
from datetime import datetime
from typing import List, Dict

class Notes:
    """Offline note-taking system"""
    
    def __init__(self, notes_dir: str = None):
        self.notes_dir = notes_dir or os.path.expanduser("~/.offnet/notes")
        os.makedirs(self.notes_dir, exist_ok=True)
    
    def create_note(self, title: str, content: str, tags: List[str] = None) -> str:
        """Create a new note"""
        note_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        note_file = os.path.join(self.notes_dir, f"{note_id}.json")
        
        note_data = {
            'id': note_id,
            'title': title,
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        with open(note_file, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)
        
        return note_id
    
    def get_note(self, note_id: str) -> Dict:
        """Get a specific note"""
        note_file = os.path.join(self.notes_dir, f"{note_id}.json")
        
        if os.path.exists(note_file):
            with open(note_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        raise FileNotFoundError(f"Note {note_id} not found")
    
    def list_notes(self, tag: str = None) -> List[Dict]:
        """List all notes, optionally filtered by tag"""
        notes = []
        
        for filename in os.listdir(self.notes_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.notes_dir, filename), 'r', encoding='utf-8') as f:
                    note = json.load(f)
                    
                    if tag is None or tag in note.get('tags', []):
                        notes.append(note)
        
        # Sort by creation date, newest first
        notes.sort(key=lambda x: x['created_at'], reverse=True)
        return notes
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by content"""
        results = []
        query_lower = query.lower()
        
        for note in self.list_notes():
            if (query_lower in note['title'].lower() or 
                query_lower in note['content'].lower() or
                any(query_lower in tag.lower() for tag in note.get('tags', []))):
                results.append(note)
        
        return results
    
    def update_note(self, note_id: str, title: str = None, content: str = None, tags: List[str] = None):
        """Update an existing note"""
        note_file = os.path.join(self.notes_dir, f"{note_id}.json")
        
        if not os.path.exists(note_file):
            raise FileNotFoundError(f"Note {note_id} not found")
        
        with open(note_file, 'r', encoding='utf-8') as f:
            note_data = json.load(f)
        
        if title is not None:
            note_data['title'] = title
        if content is not None:
            note_data['content'] = content
        if tags is not None:
            note_data['tags'] = tags
        
        note_data['updated_at'] = datetime.now().isoformat()
        
        with open(note_file, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)
    
    def delete_note(self, note_id: str):
        """Delete a note"""
        note_file = os.path.join(self.notes_dir, f"{note_id}.json")
        
        if os.path.exists(note_file):
            os.remove(note_file)
        else:
            raise FileNotFoundError(f"Note {note_id} not found")
