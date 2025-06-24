#!/usr/bin/env python3
"""
Setup script for Cross-Border Semantic Negotiation
AI-driven semantic negotiation for EU digital public services
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cross-border-semantic-negotiation",
    version="1.0.0",
    author="Cross-Border Semantic Negotiation Team",
    author_email="contact@semantic-negotiation.eu",
    description="AI-driven semantic negotiation for cross-border digital public services",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/cross-border-semantic-negotiation",
    project_urls={
        "Bug Tracker": "https://github.com/YOUR_USERNAME/cross-border-semantic-negotiation/issues",
        "Documentation": "https://cross-border-semantic-negotiation.readthedocs.io/",
        "Source Code": "https://github.com/YOUR_USERNAME/cross-border-semantic-negotiation",
        "Demo": "https://github.com/YOUR_USERNAME/cross-border-semantic-negotiation/blob/main/demo/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Sociology :: History",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-asyncio>=0.15.0", 
            "pytest-cov>=2.12.0",
            "black>=21.7.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.1.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "matplotlib>=3.4.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
        "api": [
            "fastapi>=0.70.0",
            "uvicorn>=0.15.0",
            "gunicorn>=20.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cross-border-demo=src.cross_border_implementation:demo_italy_germany_birth_certificate",
            "semantic-negotiation=src.cross_border_implementation:EuropeanDigitalServiceAgent",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "ontologies/*.owl",
            "demo/*.html",
            "docs/*.md",
            "examples/*.py",
            "examples/*.json",
        ],
    },
    zip_safe=False,
    keywords=[
        "semantic-web",
        "ontology-alignment", 
        "digital-government",
        "eu-interoperability",
        "cross-border-services",
        "ai-agents",
        "llm",
        "eidas",
        "once-only-principle",
        "public-services",
    ],
    platforms=["any"],
    license="Apache License 2.0",
)