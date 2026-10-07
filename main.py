import pandas as pd
import argparse
from pathlib import Path
import sys

from src.reader import read_excel_files
from src.validator import (
    validate_required_fields,
    validate_dates,
    validate_values,
    validate_status,
    validate_duplicates,
)
from src.consolidator import consolidate_data
from src.report import (
    generate_consolidated_report,
    generate_error_report,
)


def main(input_dir="input", output_dir="output"):

    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Erro: diretório de entrada não encontrado: {input_dir}")
        return 1

    if not input_path.is_dir():
        print(f"Erro: o caminho de entrada não é um diretório: {input_dir}")
        return 1   
   
   
    planilhas = read_excel_files(input_dir)

    if not planilhas:
        print(f"Erro: nenhuma planilha Excel encontrada em: {input_dir}")
        return 1

    print("=" * 50)
    print("EXCELFLOW - VALIDAÇÃO E CONSOLIDAÇÃO DE DADOS")
    print("=" * 50)

    print(f"\nPlanilhas encontradas: {len(planilhas)}")

    # Contadores
    total_registros = 0
    total_erros = 0
    total_datas_invalidas = 0
    total_valores_invalidos = 0
    total_status_invalidos = 0

    # Listas para armazenar os erros encontrados
    lista_erros_campos = []
    lista_erros_datas = []
    lista_erros_valores = []
    lista_erros_status = []

    # Validação individual das planilhas
    for planilha in planilhas:

        total_registros += len(planilha)

        # Campos obrigatórios
        erros = validate_required_fields(planilha)
        total_erros += len(erros)

        if not erros.empty:
            lista_erros_campos.append(erros)

            print("\nCampos obrigatórios vazios:")
            print(erros.to_string(index=False))

        # Datas
        erros_datas = validate_dates(planilha)
        total_datas_invalidas += len(erros_datas)

        if not erros_datas.empty:
            lista_erros_datas.append(erros_datas)

            print("\nDatas inválidas:")
            print(erros_datas.to_string(index=False))

        # Valores
        erros_valores = validate_values(planilha)
        total_valores_invalidos += len(erros_valores)

        if not erros_valores.empty:
            lista_erros_valores.append(erros_valores)

            print("\nValores inválidos:")
            print(erros_valores.to_string(index=False))

        # Status
        erros_status = validate_status(planilha)
        total_status_invalidos += len(erros_status)

        if not erros_status.empty:
            lista_erros_status.append(erros_status)

            print("\nStatus inválidos:")
            print(erros_status.to_string(index=False))

    # Consolida os erros encontrados
    erros_campos_completos = (
        pd.concat(lista_erros_campos, ignore_index=True)
        if lista_erros_campos
        else pd.DataFrame()
    )

    erros_datas_completos = (
        pd.concat(lista_erros_datas, ignore_index=True)
        if lista_erros_datas
        else pd.DataFrame()
    )

    erros_valores_completos = (
        pd.concat(lista_erros_valores, ignore_index=True)
        if lista_erros_valores
        else pd.DataFrame()
    )

    erros_status_completos = (
        pd.concat(lista_erros_status, ignore_index=True)
        if lista_erros_status
        else pd.DataFrame()
    )

    # Consolidação das planilhas
    base_completa = consolidate_data(planilhas)

    # Validação de duplicidades na base completa
    erros_duplicados = validate_duplicates(base_completa)

    if not erros_duplicados.empty:
        print("\nIDs duplicados:")
        print(erros_duplicados.to_string(index=False))

    total_duplicidades = (
        erros_duplicados["ID"].nunique()
        if not erros_duplicados.empty
        else 0
    )

    # Geração da base consolidada
    arquivo_consolidado = generate_consolidated_report(
        base_completa,
        output_dir=output_dir,
    )

    # Geração do relatório de erros
    arquivo_erros = generate_error_report(
        erros_campos_completos,
        erros_datas_completos,
        erros_valores_completos,
        erros_status_completos,
        erros_duplicados,
        output_dir=output_dir,
    )

    # Resumo final
    print("\n" + "=" * 50)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 50)
    print(f"Registros processados: {total_registros}")
    print(f"Campos obrigatórios vazios: {total_erros}")
    print(f"Datas inválidas: {total_datas_invalidas}")
    print(f"Valores inválidos: {total_valores_invalidos}")
    print(f"Status inválidos: {total_status_invalidos}")
    print(f"IDs duplicados: {total_duplicidades}")
    print("=" * 50)

    print("\nArquivos gerados:")
    print(f"- {arquivo_consolidado}")
    print(f"- {arquivo_erros}")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "ExcelFlow - Consolidação e validação "
            "automatizada de planilhas Excel."
        )
    )

    parser.add_argument(
        "--input",
        default="input",
        help="Diretório contendo as planilhas de entrada.",
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Diretório onde os relatórios serão gerados.",
    )

    args = parser.parse_args()

    sys.exit(
        main(
            input_dir=args.input,
            output_dir=args.output,
        )
    )