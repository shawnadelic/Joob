from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

config = {
    # General info
    "name": "joob",
    "version": "0.1",
    "description": "Joob Song Lyric Analyzer and Generator",
    "long_description": long_description,
    "license": "GPL3",

    # URL info
    "url": "https://github.com/shawnadelic/joob",
    "download_url": "https://github.com/shawnadelic/joob/archive/master.zip",

    # Author info
    "author": "Shawn Her Many Horses",
    "author_email": "shawnhmh@gmail.com",

    # Meta info 
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Linguistic",
    ],
    "keywords": "joob nltk song lyric analyzer generator natural language processing generation",

    # Package info
    "packages": ["joob"],
    "install_requires": ["nltk", "sqlalchemy"],
    "extras_require": {
        "dev": ["check-manifest"],
        "test": ["pytest"]
    },
    "entry_points": {
        "console_scripts": [
            "build_dict=joob.commands:build_dict"
        ]
    },
}

setup(**config)
