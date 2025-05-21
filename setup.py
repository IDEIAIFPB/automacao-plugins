#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="syncpl",
    version="0.1.0",
    description="Ferramenta para converter arquivos XSD em documentos de mapeamento XML",
    author="Desenvolvido Automaticamente",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "lxml>=4.9.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "syncpl=syncpl.cli:app",
        ],
    },
    python_requires=">=3.8",
    classifiers=[],
)