#!/usr/bin/env python3
import offnet

# Чат
chat = offnet.chat("DemoUser")
print("Чат создан. Используй chat.start()")

# Поиск по данным
wiki = offnet.cite('wikipedia')
results = wiki.search('python')
for r in results:
    print(f"- {r['title']}")

# Инструменты
calc = offnet.tool('calculator')
print(f"2 + 2 = {calc.calculate('2 + 2')}")
