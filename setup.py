"""Setup script for Jack compiler."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jack-compiler",
    version="1.0.0",
    author="Jack Compiler Contributors",
    description="Jack compiler for nand2tetris Hack computer using ANTLR4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jack-compiler",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "antlr4-python3-runtime==4.13.0",
    ],
    entry_points={
        "console_scripts": [
            "jackc=src.compiler:main",
        ],
    },
)
