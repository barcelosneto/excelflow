import pandas as pd


def normalize_currency(value):
    """
    Converte valores monetários para float.

    Exemplos:
    4500          -> 4500.0
    3850.50       -> 3850.5
    R$ 2.350,00   -> 2350.0
    3.900,00      -> 3900.0

    Retorna None quando o valor não puder ser convertido.
    """

    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    value = value.replace("R$", "").strip()
    value = value.replace(".", "")
    value = value.replace(",", ".")

    try:
        return float(value)
    except ValueError:
        return None


def normalize_status(value):
    """
    Padroniza diferentes formas de escrita dos status.

    Exemplos:
    Finalizado   -> Concluído
    Concluido    -> Concluído
    concluído    -> Concluído
    PENDENTE     -> Pendente
    Em Andamento -> Em andamento

    Retorna None quando o status não pertence
    aos valores reconhecidos pelo sistema.
    """

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    status_map = {
        "concluído": "Concluído",
        "concluido": "Concluído",
        "finalizado": "Concluído",

        "pendente": "Pendente",

        "em andamento": "Em andamento",
    }

    return status_map.get(value)    