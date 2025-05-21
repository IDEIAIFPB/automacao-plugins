#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich import print as rprint

from src.xsd_parser import XsdParser
from src.mapper_generator import MapperGenerator


app = typer.Typer(
    name="syncpl",
    help="Ferramenta para converter arquivos XSD em documentos de mapeamento XML."
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
    output_file: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Caminho para o arquivo XML de saída. Se não for fornecido, será usado o mesmo nome do arquivo XSD, mas com extensão .xml",
    ),
    root_element: str = typer.Option(
        ...,
        "--root", "-r",
        help="Nome do elemento raiz para iniciar o mapeamento",
    ),
    mapper_id: str = typer.Option(
        "auto-generated",
        "--id",
        help="Identificador para o documento de mapeamento",
    ),
    xpath_prefix: str = typer.Option(
        "/SynchroId/PedidoEnvioRPS/RPS",
        "--xpath-prefix", "-x",
        help="Prefixo para os caminhos XPath no documento de mapeamento",
    ),
    properties_file: Optional[Path] = typer.Option(
        None,
        "--properties", "-p",
        help="Caminho para o arquivo properties.json com mapeamentos de XPath",
        exists=False,
        readable=True,
        file_okay=True,
        dir_okay=False,
    ),
):
    """
    Gera um documento de mapeamento XML a partir de um arquivo XSD.
    """
    try:
        # Definir o arquivo de saída se não for fornecido
        if not output_file:
            output_file = xsd_file.with_suffix(".xml")
        
        with console.status(f"Analisando o arquivo XSD {xsd_file}..."):
            parser = XsdParser(str(xsd_file))
        
        with console.status(f"Gerando o documento de mapeamento..."):
            generator = MapperGenerator(parser, xpath_prefix, str(properties_file) if properties_file else None)
            generator.save_mapper_to_file(str(output_file), root_element, mapper_id)
        
        rprint(f"[green]✓[/green] Documento de mapeamento gerado com sucesso: [bold]{output_file}[/bold]")
        
    except Exception as e:
        rprint(f"[red]✗[/red] Erro: {str(e)}")
        sys.exit(1)


@app.command()
def list_elements(
    xsd_file: Path = typer.Argument(
        ...,
        help="Caminho para o arquivo XSD",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
    ),
):
    """
    Lista todos os elementos disponíveis no arquivo XSD.
    """
    try:
        with console.status(f"Analisando o arquivo XSD {xsd_file}..."):
            parser = XsdParser(str(xsd_file))
        
        elements = parser.get_root_elements()
        
        if elements:
            rprint("[bold]Elementos encontrados no XSD:[/bold]")
            for i, element in enumerate(elements, 1):
                type_info = f"[dim]({element.type})[/dim]" if element.type else ""
                complex_info = "[cyan][complexo][/cyan]" if element.is_complex else ""
                rprint(f"{i}. [green]{element.name}[/green] {type_info} {complex_info}")
        else:
            rprint("[yellow]Nenhum elemento encontrado no XSD.[/yellow]")
            
    except Exception as e:
        rprint(f"[red]✗[/red] Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()