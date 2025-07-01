# Syncpl

Uma ferramenta para converter automaticamente arquivos XSD em documentos de mapeamento XML usando o XSD.

## Instalação

### Para usuários

#### Usando pip (recomendado para usuários finais)
```bash
pip install syncpl
```

#### Usando uv
```bash
# Clone o repositório
git clone <url-do-repo>
cd automacao-plugins-main

# Execute o script de instalação
chmod +x ./install-syncpl-uv.sh
./install-syncpl-uv.sh

# Ou manualmente:
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Para desenvolvimento

Para contribuir com o desenvolvimento é necessário que:

1. Instale as dependências do projeto
    ```bash
    uv sync
    ```

2. Ative a venv
   ```bash
    source .venv/bin/activate
    ```

3. Instale o pre-commit (formatador de código)
    ```bash
    pre-commit install
    ```

## Uso

### Via linha de comando

#### Ajuda

```bash
syncpl --help
```
Isso exibirá uma lista de comandos disponíveis e suas descrições.

#### Listar elementos disponíveis no XSD

```bash
syncpl list-elements caminho/para/seu/arquivo.xsd
```
Isso exibirá uma lista de todos os elementos RAIZ disponíveis no arquivo XSD.

#### Gerar um documento de mapeamento

```bash
syncpl generate caminho/para/seu/arquivo.xsd --root NomeDoElementoRaiz --output saida.xml
```

### Parâmetros

- `--root`, `-r`: Nome do elemento raiz para iniciar o mapeamento (obrigatório).
- `--output`, `-o`: Caminho para o arquivo XML de saída. Se não for fornecido, será usado o mesmo nome do arquivo XSD, mas com extensão .xml.
- `--id`: Identificador para o documento de mapeamento (padrão: "auto-generated").
- `--xpath-prefix`, `-x`: Prefixo para os caminhos XPath no documento de mapeamento (padrão: "/SynchroId/PedidoEnvioRPS/RPS").
- `--properties`, `-p`: Caminho para o arquivo de propriedades (padrão: "properties.json"). 

## Exemplo

Arquivo xsd `nfse-v2-02.xsd` e queira gerar um mapeamento para o elemento raiz `GerarNfseEnvio`:

```bash
syncpl generate ./xsd--files/nfse-v2-02.xsd --root GerarNfseEnvio --output emissao-mapper.xml --properties properties.json
```