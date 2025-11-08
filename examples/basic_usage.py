#!/usr/bin/env python3
"""
Basic usage examples for OffNet library
"""

import offnet
from rich.console import Console

console = Console()

def demo_offworld():
    console.print("\n[bold blue]=== OffWorld Demo ===[/bold blue]")
    
    # Use Wikipedia
    try:
        wiki = offnet.cite('wikipedia')
        results = wiki.search('python programming')
        
        console.print("[green]Wikipedia Search Results:[/green]")
        for result in results:
            console.print(f"  • {result['title']}: {result['summary']}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def demo_chat():
    console.print("\n[bold blue]=== GloffChat Demo ===[/bold blue]")
    
    chat = offnet.chat("DemoUser")
    console.print("Chat created. Use chat.start() to begin chatting")

def demo_tools():
    console.print("\n[bold blue]=== Offline Tools Demo ===[/bold blue]")
    
    # Calculator
    calc = offnet.tool('calculator')
    result = calc.calculate("2 + 2 * 2")
    console.print(f"[green]Calculator: 2 + 2 * 2 = {result}[/green]")
    
    # Translator
    translator = offnet.tool('translator')
    translated = translator.translate("hello friend how are you", 'en', 'es')
    console.print(f"[green]Translator: 'hello friend how are you' -> '{translated}'[/green]")
    
    # Weather
    weather = offnet.tool('weather')
    weather_data = weather.get_weather("London")
    console.print(f"[green]Weather in London: {weather_data['temperature']}°C, {weather_data['condition']}[/green]")
    
    # Notes
    notes = offnet.tool('notes')
    note_id = notes.create_note("Test Note", "This is a test note", ["test", "demo"])
    console.print(f"[green]Created note with ID: {note_id}[/green]")

if __name__ == "__main__":
    demo_offworld()
    demo_chat() 
    demo_tools()
