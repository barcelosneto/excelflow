import pandas as pd

from src.cleaner import normalize_currency, normalize_status


COLUNAS_OBRIGATORIAS = [
    "ID",
    "Cliente",
    "Responsável",
    "Data",
    "Status",
    "Valor",
]


def validate_required_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica registros que possuem campos obrigatórios vazios.
    """

    erros = []

    for indice, linha in df.iterrows():
        for coluna in COLUNAS_OBRIGATORIAS:

            if pd.isna(linha[coluna]) or str(linha[coluna]).strip() == "":
                erros.append(
                    {
                        "linha": indice + 2,
                        "ID": linha["ID"],
                        "campo": coluna,
                        "erro": "Campo obrigatório vazio",
                        "arquivo_origem": linha["arquivo_origem"],
                    }
                )

    return pd.DataFrame(erros)


def validate_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica datas inválidas ou inexistentes.

    Campos vazios não são tratados aqui, pois já são
    identificados pela validação de campos obrigatórios.
    """

    erros = []

    for indice, linha in df.iterrows():

        data = linha["Data"]

        if pd.isna(data) or str(data).strip() == "":
            continue

        data_convertida = pd.to_datetime(
            data,
            format="%d/%m/%Y",
            errors="coerce",
        )

        if pd.isna(data_convertida):
            erros.append(
                {
                    "linha": indice + 2,
                    "ID": linha["ID"],
                    "campo": "Data",
                    "valor": data,
                    "erro": "Data inválida",
                    "arquivo_origem": linha["arquivo_origem"],
                }
            )

    return pd.DataFrame(erros)


def validate_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica valores monetários que não podem ser
    convertidos para formato numérico.
    """

    erros = []

    for indice, linha in df.iterrows():

        valor = linha["Valor"]

        # Campo vazio já é tratado pela validação
        # de campos obrigatórios.
        if pd.isna(valor) or str(valor).strip() == "":
            continue

        valor_normalizado = normalize_currency(valor)

        if valor_normalizado is None:
            erros.append(
                {
                    "linha": indice + 2,
                    "ID": linha["ID"],
                    "campo": "Valor",
                    "valor": valor,
                    "erro": "Valor monetário inválido",
                    "arquivo_origem": linha["arquivo_origem"],
                }
            )

    return pd.DataFrame(erros)


def validate_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica IDs duplicados na base consolidada.
    """

    duplicados = df[
        df.duplicated(
            subset=["ID"],
            keep=False,
        )
    ].copy()

    if duplicados.empty:
        return pd.DataFrame()

    duplicados = duplicados[
        [
            "ID",
            "Cliente",
            "arquivo_origem",
        ]
    ].sort_values("ID")

    duplicados["erro"] = "ID duplicado"

    return duplicados

def validate_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica status que não pertencem aos valores
    reconhecidos pelo sistema.
    """

    erros = []

    for indice, linha in df.iterrows():

        status = linha["Status"]

        # Campo vazio já é tratado pela validação
        # de campos obrigatórios.
        if pd.isna(status) or str(status).strip() == "":
            continue

        status_normalizado = normalize_status(status)

        if status_normalizado is None:
            erros.append(
                {
                    "linha": indice + 2,
                    "ID": linha["ID"],
                    "campo": "Status",
                    "valor": status,
                    "erro": "Status inválido",
                    "arquivo_origem": linha["arquivo_origem"],
                }
            )

    return pd.DataFrame(erros)