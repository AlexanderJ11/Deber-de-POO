import functools
from datetime import datetime


def validar_entrada(func):
    """Decorador que captura errores de entrada y muestra mensaje amigable."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"\n  ⚠ Error de valor: {e}")
        except KeyboardInterrupt:
            print("\n  Operación cancelada.")
    return wrapper


def log_operacion(func):
    """Decorador que registra en consola cuándo se ejecuta una operación."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n  [LOG] Ejecutando: {func.__name__} — {datetime.now().strftime('%H:%M:%S')}")
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper
