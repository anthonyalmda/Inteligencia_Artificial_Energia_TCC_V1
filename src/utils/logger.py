"""Configuração de logging estruturado."""
import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "energy_forecast",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configura logger estruturado.
    
    Args:
        name: Nome do logger
        level: Nível de log (logging.INFO, logging.DEBUG, etc.)
        log_file: Caminho para arquivo de log (opcional)
        format_string: String de formatação customizada (opcional)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar handlers duplicados
    if logger.handlers:
        return logger
    
    # Formato padrão
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(message)s'
        )
    
    formatter = logging.Formatter(format_string)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Logger padrão
default_logger = setup_logger()

