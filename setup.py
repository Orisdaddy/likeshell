# -*- coding: utf-8 -*-
import importlib
from setuptools import setup

DESCRIPTION = ""
VERSION = importlib.import_module('likeshell.__version__').__version__

setup(
    name='likeshell',
    version=VERSION,
    description=DESCRIPTION,
    # long_description='',
    # long_description_content_type='text/markdown',
    author="Fizone",
    author_email="edeport126@gmail.com",
    license='Apache License 2.0',
    url="https://github.com/Orisdaddy/likeshell",
    keywords=['shell', 'command', 'line'],
    packages=['likeshell'],
    include_package_data=True,
    platforms="any",
    python_requires=">=3.6",
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    )
)
