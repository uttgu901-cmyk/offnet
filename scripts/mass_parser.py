#!/usr/bin/env python3
"""
Парсит 100+ страниц и сохраняет в sites/
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time

def get_text(url):
    """Просто получает текст с сайта"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:8000]
    except:
        return None

def parse_wikipedia():
    """100+ страниц Википедии"""
    print("📚 Парсим Wikipedia...")
    
    pages = {
        # Программирование (15)
        "Python Programming": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "JavaScript": "https://en.wikipedia.org/wiki/JavaScript",
        "Java": "https://en.wikipedia.org/wiki/Java_(programming_language)",
        "C++": "https://en.wikipedia.org/wiki/C%2B%2B",
        "HTML": "https://en.wikipedia.org/wiki/HTML",
        "CSS": "https://en.wikipedia.org/wiki/CSS",
        "SQL": "https://en.wikipedia.org/wiki/SQL",
        "Git": "https://en.wikipedia.org/wiki/Git",
        "Docker": "https://en.wikipedia.org/wiki/Docker_(software)",
        "Kubernetes": "https://en.wikipedia.org/wiki/Kubernetes",
        "React": "https://en.wikipedia.org/wiki/React_(JavaScript_library)",
        "Node.js": "https://en.wikipedia.org/wiki/Node.js",
        "TypeScript": "https://en.wikipedia.org/wiki/TypeScript",
        "MongoDB": "https://en.wikipedia.org/wiki/MongoDB",
        "PostgreSQL": "https://en.wikipedia.org/wiki/PostgreSQL",
        
        # Наука (15)
        "Physics": "https://en.wikipedia.org/wiki/Physics",
        "Chemistry": "https://en.wikipedia.org/wiki/Chemistry",
        "Biology": "https://en.wikipedia.org/wiki/Biology",
        "Mathematics": "https://en.wikipedia.org/wiki/Mathematics",
        "Astronomy": "https://en.wikipedia.org/wiki/Astronomy",
        "Geology": "https://en.wikipedia.org/wiki/Geology",
        "Psychology": "https://en.wikipedia.org/wiki/Psychology",
        "Sociology": "https://en.wikipedia.org/wiki/Sociology",
        "Economics": "https://en.wikipedia.org/wiki/Economics",
        "Philosophy": "https://en.wikipedia.org/wiki/Philosophy",
        "History": "https://en.wikipedia.org/wiki/History",
        "Geography": "https://en.wikipedia.org/wiki/Geography",
        "Medicine": "https://en.wikipedia.org/wiki/Medicine",
        "Climate Change": "https://en.wikipedia.org/wiki/Climate_change",
        "Global Warming": "https://en.wikipedia.org/wiki/Global_warming",
        
        # Технологии (15)
        "Artificial Intelligence": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "Machine Learning": "https://en.wikipedia.org/wiki/Machine_learning",
        "Blockchain": "https://en.wikipedia.org/wiki/Blockchain",
        "Cryptocurrency": "https://en.wikipedia.org/wiki/Cryptocurrency",
        "Virtual Reality": "https://en.wikipedia.org/wiki/Virtual_reality",
        "Augmented Reality": "https://en.wikipedia.org/wiki/Augmented_reality",
        "Internet": "https://en.wikipedia.org/wiki/Internet",
        "World Wide Web": "https://en.wikipedia.org/wiki/World_Wide_Web",
        "Cloud Computing": "https://en.wikipedia.org/wiki/Cloud_computing",
        "Big Data": "https://en.wikipedia.org/wiki/Big_data",
        "Internet of Things": "https://en.wikipedia.org/wiki/Internet_of_things",
        "5G": "https://en.wikipedia.org/wiki/5G",
        "Quantum Computing": "https://en.wikipedia.org/wiki/Quantum_computing",
        "Robotics": "https://en.wikipedia.org/wiki/Robotics",
        "3D Printing": "https://en.wikipedia.org/wiki/3D_printing",
        
        # Культура и искусство (15)
        "Music": "https://en.wikipedia.org/wiki/Music",
        "Film": "https://en.wikipedia.org/wiki/Film",
        "Literature": "https://en.wikipedia.org/wiki/Literature",
        "Painting": "https://en.wikipedia.org/wiki/Painting",
        "Photography": "https://en.wikipedia.org/wiki/Photography",
        "Theatre": "https://en.wikipedia.org/wiki/Theatre",
        "Dance": "https://en.wikipedia.org/wiki/Dance",
        "Architecture": "https://en.wikipedia.org/wiki/Architecture",
        "Sculpture": "https://en.wikipedia.org/wiki/Sculpture",
        "Poetry": "https://en.wikipedia.org/wiki/Poetry",
        "Novel": "https://en.wikipedia.org/wiki/Novel",
        "Cinema": "https://en.wikipedia.org/wiki/Cinema",
        "Television": "https://en.wikipedia.org/wiki/Television",
        "Radio": "https://en.wikipedia.org/wiki/Radio",
        "Video Games": "https://en.wikipedia.org/wiki/Video_game",
        
        # Спорт (15)
        "Football": "https://en.wikipedia.org/wiki/Football",
        "Basketball": "https://en.wikipedia.org/wiki/Basketball",
        "Tennis": "https://en.wikipedia.org/wiki/Tennis",
        "Swimming": "https://en.wikipedia.org/wiki/Swimming",
        "Athletics": "https://en.wikipedia.org/wiki/Athletics",
        "Cycling": "https://en.wikipedia.org/wiki/Cycling",
        "Boxing": "https://en.wikipedia.org/wiki/Boxing",
        "Martial Arts": "https://en.wikipedia.org/wiki/Martial_arts",
        "Olympic Games": "https://en.wikipedia.org/wiki/Olympic_Games",
        "World Cup": "https://en.wikipedia.org/wiki/FIFA_World_Cup",
        "Cricket": "https://en.wikipedia.org/wiki/Cricket",
        "Rugby": "https://en.wikipedia.org/wiki/Rugby_football",
        "Golf": "https://en.wikipedia.org/wiki/Golf",
        "Baseball": "https://en.wikipedia.org/wiki/Baseball",
        "Hockey": "https://en.wikipedia.org/wiki/Hockey",
        
        # Еда и здоровье (15)
        "Nutrition": "https://en.wikipedia.org/wiki/Nutrition",
        "Healthy Diet": "https://en.wikipedia.org/wiki/Healthy_diet",
        "Exercise": "https://en.wikipedia.org/wiki/Exercise",
        "Yoga": "https://en.wikipedia.org/wiki/Yoga",
        "Meditation": "https://en.wikipedia.org/wiki/Meditation",
        "Cooking": "https://en.wikipedia.org/wiki/Cooking",
        "Baking": "https://en.wikipedia.org/wiki/Baking",
        "Wine": "https://en.wikipedia.org/wiki/Wine",
        "Coffee": "https://en.wikipedia.org/wiki/Coffee",
        "Tea": "https://en.wikipedia.org/wiki/Tea",
        "Chocolate": "https://en.wikipedia.org/wiki/Chocolate",
        "Pizza": "https://en.wikipedia.org/wiki/Pizza",
        "Sushi": "https://en.wikipedia.org/wiki/Sushi",
        "Veganism": "https://en.wikipedia.org/wiki/Veganism",
        "Vegetarianism": "https://en.wikipedia.org/wiki/Vegetarianism",
        
        # Путешествия (10)
        "Tourism": "https://en.wikipedia.org/wiki/Tourism",
        "Travel": "https://en.wikipedia.org/wiki/Travel",
        "Aviation": "https://en.wikipedia.org/wiki/Aviation",
        "Rail Transport": "https://en.wikipedia.org/wiki/Rail_transport",
        "Cruise Ship": "https://en.wikipedia.org/wiki/Cruise_ship",
        "Hotel": "https://en.wikipedia.org/wiki/Hotel",
        "Backpacking": "https://en.wikipedia.org/wiki/Backpacking",
        "Ecotourism": "https://en.wikipedia.org/wiki/Ecotourism",
        "Passport": "https://en.wikipedia.org/wiki/Passport",
        "Visa": "https://en.wikipedia.org/wiki/Visa_(document)"
    }
    
    articles = {}
    count = 0
    
    for title, url in pages.items():
        text = get_text(url)
        if text:
            articles[title] = {
                "content": text,
                "summary": text[:300] + "...",
                "url": url
            }
            count += 1
            print(f"✅ {title} ({count}/100+)")
        else:
            print(f"❌ {title}")
        
        time.sleep(1)  # Чтобы не заблокировали
    
    content = {
        "metadata": {
            "last_updated": datetime.now().isoformat(),
            "total_articles": len(articles),
            "source": "Wikipedia"
        },
        "content": {
            "articles": articles
        }
    }
    
    os.makedirs("sites/wikipedia", exist_ok=True)
    with open("sites/wikipedia/content.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 Wikipedia: {len(articles)} статей сохранено!")

def main():
    parse_wikipedia()
    print("✨ Все данные обновлены в папке sites/")

if __name__ == "__main__":
    main()
