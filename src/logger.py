import logging
from pathlib import Path


def setup_logger(
    name: str = "excelflow",
    log_dir: str = "logs",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configura o logger da aplicação.

    Os logs são enviados simultaneamente para o terminal
    e para o arquivo logs/excelflow.log.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita handlers duplicados caso a função seja chamada novamente.
    if logger.handlers:
        return logger

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_path / "excelflow.log",
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger