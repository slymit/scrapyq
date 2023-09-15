import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as handle:
    readme = handle.read()

setup(
    name='scrapyq',
    version='1.0.0',
    description='A library to filter SQLAlchemy queries.',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='slymit',
    author_email='slymit@gmail.com',
    maintainer='slymit',
    maintainer_email='slymit@gmail.com',
    url='https://github.com/slymit/scrapyq',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['scrapyd==1.4.2', 'redis==5.0.0'],
    extras_require={
        'dev': [
            'pytest==7.4.2',
            'packaging==23.1',
            'coverage>=7.2.7',
            'flake8',
            'restructuredtext-lint',
        ],
    },
    zip_safe=True,
    license='BSD',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
