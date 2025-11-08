from setuptools import setup, find_packages

setup(
    name="offnet",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
    ],
    entry_points={
        'console_scripts': [
            'gloff-chat=offnet.chat.gloff_chat:main',
        ],
    },
)
