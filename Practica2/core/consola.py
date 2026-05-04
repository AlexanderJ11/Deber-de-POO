"""
consola.py — Utilidades de terminal: colores ANSI, gotoxy y limpieza de pantalla.
Compatible con Windows (colorama) y Linux/Mac (ANSI nativo).
"""
import os
import sys

# Intentar activar colorama en Windows
try:
    import colorama
    colorama.init(autoreset=True)
except ImportError:
    pass


# ── Códigos ANSI ──────────────────────────────────────────────────────────────

class Color:
    RESET      = "\033[0m"
    NEGRITA    = "\033[1m"
    # Texto
    NEGRO      = "\033[30m"
    ROJO       = "\033[31m"
    VERDE      = "\033[32m"
    AMARILLO   = "\033[33m"
    AZUL       = "\033[34m"
    MAGENTA    = "\033[35m"
    CIAN       = "\033[36m"
    BLANCO     = "\033[37m"
    # Texto brillante
    ROJO_B     = "\033[91m"
    VERDE_B    = "\033[92m"
    AMARILLO_B = "\033[93m"
    AZUL_B     = "\033[94m"
    MAGENTA_B  = "\033[95m"
    CIAN_B     = "\033[96m"
    BLANCO_B   = "\033[97m"
    # Fondo
    BG_AZUL    = "\033[44m"
    BG_VERDE   = "\033[42m"
    BG_ROJO    = "\033[41m"
    BG_NEGRO   = "\033[40m"
    BG_CIAN    = "\033[46m"


def c(texto, *estilos):
    """Envuelve texto con uno o más estilos ANSI y resetea al final."""
    return "".join(estilos) + str(texto) + Color.RESET


# ── Cursor / pantalla ─────────────────────────────────────────────────────────

def limpiar():
    """Borra la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def gotoxy(x, y):
    """Posiciona el cursor en columna x, fila y (base 1)."""
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()


def ocultar_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def mostrar_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def pausa(mensaje="  Presione ENTER para continuar..."):
    print(c(f"\n{mensaje}", Color.AMARILLO_B))
    input()


# ── Alineación con texto ANSI ─────────────────────────────────────────────────
import re as _re

def ansi_len(texto):
    """Longitud visible de un string ignorando códigos de escape ANSI."""
    return len(_re.sub(r'\033\[[0-9;]*m', '', texto))

def ansi_ljust(texto, ancho):
    """Equivalente a str.ljust(ancho) pero ignora los códigos ANSI al contar."""
    padding = max(0, ancho - ansi_len(texto))
    return texto + ' ' * padding

def fila(*celdas):
    """
    Imprime una fila de tabla con celdas alineadas.
    Uso: fila((texto, ancho), (texto, ancho), ...)
    """
    print('  ' + ''.join(ansi_ljust(t, a) for t, a in celdas))
