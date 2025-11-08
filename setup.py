from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="offnet",
    version="0.1.0",
    author="OffNet Team",
    author_email="contact@example.com",
    description="Offline-first Python library with local web content and mesh chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
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
