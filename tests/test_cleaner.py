from src.cleaner import normalize_currency, normalize_status


def test_normalize_currency_number():
    assert normalize_currency(4500) == 4500.0


def test_normalize_currency_brazilian_format():
    assert normalize_currency("R$ 2.350,00") == 2350.0


def test_normalize_currency_without_symbol():
    assert normalize_currency("3.900,00") == 3900.0


def test_normalize_currency_invalid():
    assert normalize_currency("cinco mil") is None


def test_normalize_status_completed():
    assert normalize_status("Finalizado") == "Concluído"
    assert normalize_status("Concluido") == "Concluído"
    assert normalize_status("concluído") == "Concluído"


def test_normalize_status_pending():
    assert normalize_status("PENDENTE") == "Pendente"


def test_normalize_status_in_progress():
    assert normalize_status("Em Andamento") == "Em andamento"


def test_normalize_status_invalid():
    assert normalize_status("Aguardando") is None