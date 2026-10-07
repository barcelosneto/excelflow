import pandas as pd

from src.consolidator import consolidate_data


def test_consolidate_data():
    df_sp = pd.DataFrame(
        {
            "ID": ["SP-1001", "SP-1002"],
            "Cliente": ["Empresa A", "Empresa B"],
            "Responsável": ["Ana", "Carlos"],
            "Data": ["01/10/2026", "02/10/2026"],
            "Status": ["Concluído", "Pendente"],
            "Valor": [4500, 7200],
            "arquivo_origem": ["filial_sp.xlsx", "filial_sp.xlsx"],
        }
    )

    df_rj = pd.DataFrame(
        {
            "ID": ["RJ-2001", "RJ-2002"],
            "Cliente": ["Empresa C", "Empresa D"],
            "Responsável": ["Mariana", "João"],
            "Data": ["03/10/2026", "04/10/2026"],
            "Status": ["Em andamento", "Concluído"],
            "Valor": [5000, 8300],
            "arquivo_origem": ["filial_rj.xlsx", "filial_rj.xlsx"],
        }
    )

    resultado = consolidate_data([df_sp, df_rj])

    assert len(resultado) == 4
    assert list(resultado["ID"]) == [
        "SP-1001",
        "SP-1002",
        "RJ-2001",
        "RJ-2002",
    ]

    assert resultado.iloc[0]["arquivo_origem"] == "filial_sp.xlsx"
    assert resultado.iloc[2]["arquivo_origem"] == "filial_rj.xlsx"