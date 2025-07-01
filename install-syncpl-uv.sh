#!/bin/bash
# Script para instalar o syncpl usando uv

echo "🚀 Instalando syncpl com uv..."

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    uv venv
fi

# Ativar ambiente virtual e instalar
echo "⚙️  Instalando pacote..."
source .venv/bin/activate
uv pip install -e .

echo "✅ Instalação concluída!"
echo ""
echo "Para usar o comando syncpl:"
echo "1. Ative o ambiente virtual: source .venv/bin/activate"
echo "2. Execute: syncpl --help"
echo ""
echo "Ou execute diretamente do ambiente virtual:"
echo "   .venv/bin/syncpl --help"
