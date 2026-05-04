import sys
import os

# Permite importar desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from views.menu import menu_principal

if __name__ == "__main__":
    menu_principal()
