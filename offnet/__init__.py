"""
OffNet - Offline-first Python library with local web content and mesh chat
"""

__version__ = "0.1.0"
__author__ = "OffNet Team"

from offnet.core import OffWorld, update_all_content
from offnet.chat.gloff_chat import GloffChat
from offnet.cite.re_cite import Recite
from offnet.tools.calculator import Calculator
from offnet.tools.translator import Translator
from offnet.tools.weather import Weather
from offnet.tools.notes import Notes

# Global instance
offworld = OffWorld()

# Shortcut functions
def cite(site_name):
    """Import a site for offline use"""
    return offworld.cite(site_name)

def chat(username="Anonymous"):
    """Start GloffChat"""
    return GloffChat(username)

def tool(tool_name):
    """Access offline tools"""
    return offworld.get_tool(tool_name)

__all__ = [
    'offworld', 'cite', 'chat', 'tool',
    'OffWorld', 'GloffChat', 'Recite', 
    'Calculator', 'Translator', 'Weather', 'Notes',
    'update_all_content'
]
