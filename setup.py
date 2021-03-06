#!/usr/bin/env python3
''' setup file for installation of niiview '''
from setuptools import setup, find_packages

setup(
    name='niiview',
    version='1.0.1',
    description='Display NIfTI images in sixel-aware terminals.',
    author='Tobias Kadelka',
    author_email='t.kadelka@fz-juelich.de',
    packages=find_packages(),
    license='ISC',
    install_requires=[
        'nibabel',
        'matplotlib',
        'numpy',
        'libsixel-python',
        'getkey',
        'Pillow'
    ],
    python_requires=">=3.0",
    scripts=[
        'niiview'
    ],
    data_files=[
        ('share/man/man1', ['niiview.1'])
    ]
)
