# Syncpl

Uma ferramenta para converter automaticamente arquivos XSD em documentos de mapeamento XML usando o XSD.

## Instalação

Para instalar a ferramenta, clone o repositório e instale usando pip:

```bash
# Clone o repositório
git clone <url-do-repositório>

# Entre no diretório
cd syncpl

# Instale o pacote em modo de desenvolvimento
pip install -e .
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