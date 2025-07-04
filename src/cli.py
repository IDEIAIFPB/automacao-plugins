#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich import print as rprint

from src.mapper import Mapper

from src.core.utils.constants import build_output_file_path


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
    )
):
    """
    Gera um documento de mapeamento XML a partir de um arquivo XSD.
    """
    try:
        with console.status("Construindo o parser"):
            parser = Mapper(
                root_element,
                plugin_name,
                xsd_file,
                output_file
            )
        
        with console.status(f"Gerando arvore do xml"):
            tree = parser.build()

        with console.status("Gerando o documento de mapeamento..."):
            xml_content = parser.build_xml(tree)
        
        with console.status(f"Exportando o documento para: {xsd_file}"):
            parser.export_xml_to_file(xml_content, output_file)

        console.status(f"Resultado:\n{xml_content}")

        rprint(
            f"[green]✓[/green] Documento de mapeamento gerado com sucesso: [bold]{output_file}[/bold]"
        )

    except Exception as e:
        rprint(f"[red]✗[/red] Erro: {str(e)}")
        sys.exit(1)


# @app.command()
# def list_elements(
#     xsd_file: Path = typer.Argument(
#         ...,
#         help="Caminho para o arquivo XSD",
#         exists=True,
#         readable=True,
#         file_okay=True,
#         dir_okay=False,
#     ),
# ):
#     """
#     Lista todos os elementos disponíveis no arquivo XSD.
#     """
#     try:
#         with console.status(f"Analisando o arquivo XSD {xsd_file}..."):
#             parser = XsdParser(str(xsd_file))

#         elements = parser.get_root_elements()

#         if elements:
#             rprint("[bold]Elementos encontrados no XSD:[/bold]")
#             for i, element in enumerate(elements, 1):
#                 type_info = f"[dim]({element.type})[/dim]" if element.type else ""
#                 complex_info = "[cyan][complexo][/cyan]" if element.is_complex else ""
#                 rprint(f"{i}. [green]{element.name}[/green] {type_info} {complex_info}")
#         else:
#             rprint("[yellow]Nenhum elemento encontrado no XSD.[/yellow]")

#     except Exception as e:
#         rprint(f"[red]✗[/red] Erro: {str(e)}")
#         sys.exit(1)


if __name__ == "__main__":
    # app()
    
    generate(
        xsd_file="resources/xsd-files/NFSE.xsd.XSD",
        output_file=build_output_file_path("cli.xml"),
        root_element="EnviarLoteRpsEnvio",
        plugin_name="teste"
    )
