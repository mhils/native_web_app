#!/usr/bin/env python3
import re
from pathlib import Path

from setuptools import setup

here = Path(__file__).parent

VERSION = re.search(
    r'__version__ = "(.+?)"', (here / "native_web_app.py").read_text()
).group(1)

long_description = (here / "README.md").read_text()

setup(
    name="native_web_app",
    version=VERSION,
    description="Build Electron-like apps without Electron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
    ],
    keywords="webbrowser electron browser pwa webapp",
    url="https://github.com/mhils/native_web_app",
    author="Maximilian Hils",
    author_email="pypi@maximilianhils.com",
    license="MIT",
    py_modules=["native_web_app"],
    python_requires='>=3.7',
)
