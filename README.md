# Syncpl

Uma ferramenta para converter automaticamente arquivos XSD em documentos de mapeamento XML usando o XSD.

## Instalação

Para contribuir com o desenvolvimento é necessáiro que:

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

#### Gerar um Plugin

```bash
#comando básico
syncpl generate caminho/para/arquivo.xsd --root NomeDoElementoRaiz --output saida.xml

# Comando completo com action
syncpl generate resources/xsd-files/NFSE.xsd \
  --root EnviarLoteRpsEnvio \
  --output cli.xml \
  --id emissao-campina \
  --operation RecepcionarLoteRps \
  --response EnviarLoteRpsResposta \
  --wsdl resources/wsdl-files/nfse04.wsdl \
  --action-output cli-action.xml \
  --targets '{"numero_param": "NumeroLote", "protocolo_param": "Protocolo"}'
```

### Parâmetros

**Obrigatórios:**
- `xsd_file`: Caminho para o arquivo XSD de entrada (argumento posicional)
- `--root`, `-r`: Nome do elemento raiz para iniciar o mapeamento

**Opcionais:**
- `--output`, `-o`: Caminho para o arquivo XML de saída (padrão: mesmo nome do XSD com extensão .xml)
- `--id`: Identificador para o documento de mapeamento (padrão: "auto-generated")
- `--operation`: Tag referente à operação desejada (para geração de action)
- `--response`: Tag inicial do xml de resposta da prefeitura (para geração de action)
- `--wsdl`: Caminho para o arquivo WSDL referente ao plugin (para geração de action)
- `--action-output`: Caminho para o arquivo XML de saída do action
- `--targets`: Dicionário com tags finais em formato JSON (para geração de action)

**Nota:** Para gerar o arquivo action, todos os parâmetros relacionados ao action são obrigatórios: `--operation`, `--response`, `--wsdl`, `--action-output` e `--targets`.

## Exemplo

Arquivo xsd `nfse.xsd` e queira gerar um mapeamento para o elemento raiz `EnviarLoteRpsEnvio`:

```bash
syncpl generate resources/xsd-files/NFSE.xsd cli.xml EnviarLoteRpsEnvio emissao-campina RecepcionarLoteRps EnviarLoteRpsResposta resources/wsdl-files/nfse04.wsdl cli-action.xml '{
            "numero_param": "NumeroLote",
            "protocolo_param": "Protocolo",
            "aliquota_param": "Aliquota",
            "codigo_verificacao_param": "CodigoVerificacao",
            "codigo_details": "Codigo",
            "mensagem_detail": "Mensagem",
            "correcao_details": "Correcao",
            "numero_consulta": "NumeroLote",
            "codigo_cancelamento_consulta": "Codigo",
            "codigo_consulta": "Codigo",
            "data_hora": "DataHora",
            "codigo_cancelamento": "Codigo",
            "codigo_emissao": "Codigo",
            "numero_emissao": "NumeroLote"
        }'
```