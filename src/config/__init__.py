"""Configuração do projeto."""
import yaml
from pathlib import Path
from typing import Dict, Any

_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "default.yaml"

def load_config(path: Path = None) -> Dict[str, Any]:
    """Carrega configuração do arquivo YAML."""
    if path is None:
        path = _CONFIG_PATH
    
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

