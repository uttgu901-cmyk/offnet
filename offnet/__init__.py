from offnet.core import OffWorld, update_all_content
from offnet.chat.gloff_chat import GloffChat
from offnet.tools.calculator import Calculator
from offnet.tools.translator import Translator
from offnet.tools.weather import Weather
from offnet.tools.notes import Notes

offworld = OffWorld()

def cite(site_name):
    return offworld.cite(site_name)

def chat(username="Anonymous"):
    return GloffChat(username)

def tool(tool_name):
    return offworld.get_tool(tool_name)

__all__ = ['offworld', 'cite', 'chat', 'tool', 'GloffChat', 'update_all_content']
