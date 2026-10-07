import pandas as pd

from src.validator import (
    validate_required_fields,
    validate_dates,
    validate_values,
    validate_status,
    validate_duplicates,
)


def criar_dataframe():
    return pd.DataFrame(
        {
            "ID": ["SP-1001", "SP-1002", "SP-1003"],
            "Cliente": ["Empresa A", "Empresa B", "Empresa C"],
            "Responsável": ["Ana", None, "Carlos"],
            "Data": ["01/10/2026", "31/02/2026", "03/10/2026"],
            "Status": ["Concluído", "Aguardando", "Pendente"],
            "Valor": [4500, "cinco mil", "R$ 2.350,00"],
            "arquivo_origem": [
                "teste1.xlsx",
                "teste1.xlsx",
                "teste1.xlsx",
            ],
        }
    )


def test_required_fields():
    df = criar_dataframe()

    erros = validate_required_fields(df)

    assert len(erros) == 1
    assert erros.iloc[0]["ID"] == "SP-1002"
    assert erros.iloc[0]["campo"] == "Responsável"


def test_invalid_date():
    df = criar_dataframe()

    erros = validate_dates(df)

    assert len(erros) == 1
    assert erros.iloc[0]["ID"] == "SP-1002"
    assert erros.iloc[0]["valor"] == "31/02/2026"


def test_invalid_value():
    df = criar_dataframe()

    erros = validate_values(df)

    assert len(erros) == 1
    assert erros.iloc[0]["ID"] == "SP-1002"
    assert erros.iloc[0]["valor"] == "cinco mil"


def test_invalid_status():
    df = criar_dataframe()

    erros = validate_status(df)

    assert len(erros) == 1
    assert erros.iloc[0]["ID"] == "SP-1002"
    assert erros.iloc[0]["valor"] == "Aguardando"


def test_duplicates():
    df = pd.DataFrame(
        {
            "ID": ["SP-1001", "SP-1002", "SP-1001"],
            "Cliente": [
                "Empresa A",
                "Empresa B",
                "Empresa A",
            ],
            "arquivo_origem": [
                "filial_sp.xlsx",
                "filial_rj.xlsx",
                "filial_mg.xlsx",
            ],
        }
    )

    erros = validate_duplicates(df)

    assert len(erros) == 2
    assert erros["ID"].nunique() == 1
    assert erros.iloc[0]["ID"] == "SP-1001"