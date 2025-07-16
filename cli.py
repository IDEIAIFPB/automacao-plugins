#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Adiciona o diretório do projeto ao sys.path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

from src.syncpl import main as syncpl_main

def main():
    syncpl_main()

if __name__ == "__main__":
    main()