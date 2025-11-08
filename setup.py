from setuptools import setup, find_packages

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
