try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Joob',
    'author': 'shawnadelic',
    'url': 'http://shawnhmh.com',
    'download_url': 'https://github.com/shawnadelic/joob',
    'author_email': 'shawnhmh@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['joob'],
    'scripts': [],
    'name': 'joob',
}

setup(**config)
