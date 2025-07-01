#!/bin/sh

for plugin in $(ls plugins/); do
    for arquivo in plugins/$plugin/arquivos/*mapper.xml; do
        sudo python3 ./alimentacao.py "$arquivo"
    done
    echo "properties do plugin $plugin mapeadas"
done