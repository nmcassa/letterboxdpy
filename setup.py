from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text()

setup(
    name='letterboxdpy',
    version='1.1',
    license='MIT',
    author="Nicholas Cassarino",
    author_email='nmcassa804@outlook.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/nmcassa/letterboxdpy',
    keywords='webscraper letterboxd movies',
    install_requires=[
          'requests',
          'bs4',
          'json',
          're',
          
      ],
    long_description=long_description,
    long_description_content_type='text/markdown'

)
