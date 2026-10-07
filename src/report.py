from pathlib import Path
import pandas as pd


def generate_consolidated_report(
    df: pd.DataFrame,
    output_dir="output",
):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    arquivo = output_path / "base_consolidada.xlsx"

    df.to_excel(arquivo, index=False)

    return str(arquivo)


def generate_error_report(
    erros_campos,
    erros_datas,
    erros_valores,
    erros_status,
    erros_duplicados,
    output_dir="output",
):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    arquivo = output_path / "relatorio_erros.xlsx"

    with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:

        erros_campos.to_excel(
            writer,
            sheet_name="Campos obrigatórios",
            index=False,
        )

        erros_datas.to_excel(
            writer,
            sheet_name="Datas inválidas",
            index=False,
        )

        erros_valores.to_excel(
            writer,
            sheet_name="Valores inválidos",
            index=False,
        )

        erros_status.to_excel(
            writer,
            sheet_name="Status inválidos",
            index=False,
        )

        erros_duplicados.to_excel(
            writer,
            sheet_name="IDs duplicados",
            index=False,
        )

    return str(arquivo)