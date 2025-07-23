#!.venv/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console

from src.action import Action
from src.mapper import Mapper

app = typer.Typer(
    name="syncpl",
    help="Ferramenta para converter arquivos XSD em documentos de mapeamento XML.",
)
console = Console()


@app.command()
def generate(
    xsd_file: Path = typer.Argument(
        ...,
        help="Caminho para o arquivo XSD de entrada",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_file: Path = typer.Argument(
        None,
        help="Caminho para o arquivo XML de saída. Se não for fornecido, será usado o mesmo nome do arquivo XSD, mas com extensão .xml",
    ),
    root_element: str = typer.Argument(
        ...,
        help="Nome do elemento raiz para iniciar o mapeamento",
    ),
    plugin_name: str = typer.Argument(
        "auto-generated",
        help="Identificador para o documento de mapeamento",
    ),
    operation_tag: str = typer.Argument(None, help="Tag referente a operação desejada"),
    response_tag: str = typer.Argument(None, help="Tag inicial do xml de resposta da prefeitura"),
    wsdl_path: str = typer.Argument(None, help="Caminho para o arquivo wsdl referente ao plugin"),
    action_output_file: Path = typer.Argument(None, help="Caminho para o arquivo XML de saída do action."),
    targets_tags: str = typer.Argument(
        None, help="Dicionário com tags finais para parametros, condições e detalhes do mapper"
    ),
):
    """
    Gera um documento de mapeamento XML a partir de um arquivo XSD.
    """
    try:
        with console.status("Construindo o parser"):
            parser = Mapper(root_element, plugin_name, xsd_file, output_file)

        with console.status("Gerando arvore do xml"):
            tree = parser.build()

        with console.status("Gerando o documento de mapeamento..."):
            xml_content = parser.build_xml(tree)

        with console.status(f"Exportando o documento para: {xsd_file}"):
            parser.export_xml_to_file(xml_content, output_file)

        console.status(f"Resultado:\n{xml_content}")

        rprint(f"[green]✓[/green] Documento de mapeamento gerado com sucesso: [bold]{output_file}[/bold]")

        if targets_tags:
            try:
                targets_tags = json.loads(targets_tags)
            except json.JSONDecodeError:
                rprint("[red]✗[/red] Erro: Formato inválido para targets_tags. Deve ser um JSON válido.")
                sys.exit(1)

        if operation_tag and response_tag and wsdl_path and action_output_file and targets_tags:
            signatures = parser._mapper_builder.metadata.signature

            with console.status("Parseando o arquivo wsdl para criar o action"):
                action_parser = Action(
                    operation_tag,
                    response_tag,
                    wsdl_path,
                    signatures,
                    plugin_name,
                    xsd_file,
                    root_element,
                    tree,
                    targets_tags,
                )

            with console.status("Gerando arvore do xml"):
                action_tree = action_parser.build()

            with console.status("Gerando o documento de mapeamento..."):
                action_xml_content = action_parser.build_xml(action_tree)

            with console.status(f"Exportando o documento para: {xsd_file}"):
                action_parser.export_xml_to_file(action_xml_content, action_output_file)

            console.status(f"Resultado:\n{action_xml_content}")

            rprint(f"[green]✓[/green] Documento de mapeamento gerado com sucesso: [bold]{action_output_file}[/bold]")

    except Exception as e:
        rprint(f"[red]✗[/red] Erro: {str(e)}")
        sys.exit(1)


@app.command()
def list_elements(
    xsd_file: Path = typer.Argument(
        ...,
        help="Caminho para o arquivo XSD",
        # exists=True,
        # readable=True,
        # file_okay=True,
        # dir_okay=False,
    ),
):
    """
    Lista todos os elementos disponíveis no arquivo XSD.
    """
    print("Funcionalidade nao implementada ainda")
    # try:
    #     with console.status(f"Analisando o arquivo XSD {xsd_file}..."):
    #         parser = XsdParser(str(xsd_file))

    #     elements = parser.get_root_elements()

    #     if elements:
    #         rprint("[bold]Elementos encontrados no XSD:[/bold]")
    #         for i, element in enumerate(elements, 1):
    #             type_info = f"[dim]({element.type})[/dim]" if element.type else ""
    #             complex_info = "[cyan][complexo][/cyan]" if element.is_complex else ""
    #             rprint(f"{i}. [green]{element.name}[/green] {type_info} {complex_info}")
    #     else:
    #         rprint("[yellow]Nenhum elemento encontrado no XSD.[/yellow]")

    # except Exception as e:
    #     rprint(f"[red]✗[/red] Erro: {str(e)}")
    #     sys.exit(1)


def main():
    app()
    # generate(
    #     xsd_file="resources/xsd-files/NFSE.xsd.XSD",
    #     output_file=build_output_file_path("cli.xml"),
    #     root_element="EnviarLoteRpsEnvio",
    #     plugin_name="emissao-campina",
    #     operation_tag="RecepcionarLoteRps",
    #     response_tag="EnviarLoteRpsResposta",
    #     wsdl_path="resources/wsdl-files/nfse04.wsdl",
    #     action_output_file=build_output_file_path("cli-action.xml"),
    #     targets_tags=json.dumps({
    #         "numero_param": "NumeroLote",
    #         "protocolo_param": "Protocolo",
    #         "aliquota_param": "Aliquota",
    #         "codigo_verificacao_param": "CodigoVerificacao",
    #         "codigo_details": "Codigo",
    #         "mensagem_details": "Mensagem",
    #         "correcao_details": "Correcao",
    #         "numero_consulta": "NumeroLote",
    #         "codigo_cancelamento_consulta": "Codigo",
    #         "codigo_consulta": "Codigo",
    #         "data_hora": "DataHora",
    #         "codigo_cancelamento": "Codigo",
    #         "codigo_emissao": "Codigo",
    #         "numero_emissao": "NumeroLote"
    #     }),
    # )


if __name__ == "__main__":
    main()
