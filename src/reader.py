from pathlib import Path

import pandas as pd


def read_excel_files(input_dir: str) -> list[pd.DataFrame]:
    """
    Lê todos os arquivos .xlsx existentes no diretório informado.

    Cada planilha é carregada como um DataFrame e recebe
    uma coluna indicando seu arquivo de origem.
    """

    input_path = Path(input_dir)

    excel_files = list(input_path.glob("*.xlsx"))

    if not excel_files:
        raise FileNotFoundError(
            f"Nenhuma planilha encontrada em: {input_path}"
        )

    dataframes = []

    for file_path in excel_files:
        df = pd.read_excel(file_path)

        df["arquivo_origem"] = file_path.name

        dataframes.append(df)

    return dataframes