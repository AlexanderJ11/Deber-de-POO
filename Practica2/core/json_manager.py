import json
import os


class JsonManager:
    BASE = os.path.join(os.path.dirname(__file__), "..", "data")

    @staticmethod
    def _ruta(archivo):
        return os.path.join(JsonManager.BASE, archivo)

    @staticmethod
    def leer(archivo):
        ruta = JsonManager._ruta(archivo)
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def escribir(archivo, datos):
        ruta = JsonManager._ruta(archivo)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
