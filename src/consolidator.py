import pandas as pd

from src.cleaner import normalize_currency, normalize_status


def consolidate_data(planilhas: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Consolida todas as planilhas em um único DataFrame
    e aplica as padronizações conhecidas pelo ExcelFlow.

    O objetivo desta função não é excluir erros,
    mas preparar uma base única e normalizada.
    """

    if not planilhas:
        return pd.DataFrame()

    base = pd.concat(
        planilhas,
        ignore_index=True
    )

    # Preserva os valores originais para auditoria
    base["Status_original"] = base["Status"]
    base["Valor_original"] = base["Valor"]

    # Padroniza os status reconhecidos
    base["Status"] = base["Status"].apply(
        normalize_status
    )

    # Padroniza os valores monetários
    base["Valor"] = base["Valor"].apply(
        normalize_currency
    )

    return base