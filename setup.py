#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='cronls',
    packages=["cronls"],
    description='Scan and print all cron tasks',
    author='Alex Left',
    author_email='aizquierdo@mrmilu.com',
    url='https://github.com/mrmilu/cronls',
    version='0.1',
    license='GPL-v3',
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'cronls=cronls.main:main',
        ],
    },

)
