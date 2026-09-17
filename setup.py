#!/usr/bin/env python3
# setup.py

from setuptools import setup, find_packages

setup(
    name='uniqparser',
    version='1.0.0',
    description='Уникальные IP-адреса из файла с Nmap-сканированием',
    author='ultimate lizzard',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'uniqparser=main:main',
        ],
    },
    python_requires='>=3.6',
)
