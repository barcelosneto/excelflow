from pathlib import Path

import pandas as pd

from src.reader import read_excel_files
from src.consolidator import consolidate_data
from src.validator import (
    validate_required_fields,
    validate_dates,
    validate_values,
    validate_status,
    validate_duplicates,
)


def test_excel_pipeline(tmp_path):
    # -------------------------
    # Arrange
    # -------------------------

    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    filial_sp = pd.DataFrame(
        {
            "ID": ["SP-1001", "SP-1002"],
            "Cliente": ["Empresa A", "Empresa B"],
            "Responsável": ["Ana", "Carlos"],
            "Data": ["01/10/2026", "02/10/2026"],
            "Status": ["Concluído", "Pendente"],
            "Valor": [4500, 7200],
        }
    )

    filial_rj = pd.DataFrame(
        {
            "ID": ["RJ-2001", "RJ-2002"],
            "Cliente": ["Empresa C", "Empresa D"],
            "Responsável": ["Mariana", "João"],
            "Data": ["03/10/2026", "04/10/2026"],
            "Status": ["Em andamento", "Concluído"],
            "Valor": [5000, 8300],
        }
    )

    filial_sp.to_excel(
        input_dir / "filial_sp.xlsx",
        index=False,
    )

    filial_rj.to_excel(
        input_dir / "filial_rj.xlsx",
        index=False,
    )

    # -------------------------
    # Act
    # -------------------------

    planilhas = read_excel_files(str(input_dir))

    assert len(planilhas) == 2

    base = consolidate_data(planilhas)

    arquivo_saida = output_dir / "base_consolidada.xlsx"

    base.to_excel(
        arquivo_saida,
        index=False,
    )

    # -------------------------
    # Assert
    # -------------------------

    assert arquivo_saida.exists()

    resultado = pd.read_excel(arquivo_saida)

    assert len(resultado) == 4

    assert set(resultado["ID"]) == {
        "SP-1001",
        "SP-1002",
        "RJ-2001",
        "RJ-2002",
    }

    assert validate_required_fields(base).empty
    assert validate_dates(base).empty
    assert validate_values(base).empty
    assert validate_status(base).empty
    assert validate_duplicates(base).empty