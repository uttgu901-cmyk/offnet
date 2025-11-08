from setuptools import setup, find_packages

setup(
    name="offnet",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3", 
        "lxml>=4.6.3",
        "zeroconf>=0.28.0",
        "python-socketio>=5.0.0",
        "rich>=10.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'gloff-chat=offnet.chat.gloff_chat:main',
            'offnet-update=offnet.core:update_all_content_cli',
        ],
    },
)
