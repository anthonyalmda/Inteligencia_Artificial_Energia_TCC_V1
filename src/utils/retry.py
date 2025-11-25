"""Utilitário para retry com backoff exponencial em requisições."""
import time
from functools import wraps
from typing import Callable, Type, Tuple, Optional

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator para retry com backoff exponencial.
    
    Args:
        max_retries: Número máximo de tentativas
        base_delay: Delay inicial em segundos
        max_delay: Delay máximo em segundos
        exceptions: Tupla de exceções para capturar
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(min(delay, max_delay))
                        delay *= 2  # Backoff exponencial
                    else:
                        raise
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

