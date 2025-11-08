from setuptools import setup, find_packages
import subprocess
import sys

# ЗАПУСКАЕМ ПАРСЕР ПРИ УСТАНОВКЕ
def download_initial_content():
    try:
        print("📥 Downloading initial content...")
        subprocess.check_call([sys.executable, "scripts/mass_parser.py"])
    except:
        print("⚠️  Could not download content. Run manually: python scripts/mass_parser.py")

# Вызываем при установке
download_initial_content()

setup(
    name="offnet",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "rich>=10.0.0",
    ],
    entry_points={
        'console_scripts': [
            'gloff-chat=offnet.chat.gloff_chat:main',
            'offnet-update=scripts.mass_parser:main',
        ],
    },
)
