from core import ICrud, JsonManager, log_operacion
from models import Empleado

ARCHIVO = "empleados.json"


class EmpleadoController(ICrud):

    def _siguiente_id(self, lista):
        return max((e["id"] for e in lista), default=0) + 1

    @log_operacion
    def crear(self, entidad: Empleado):
        datos = JsonManager.leer(ARCHIVO)
        entidad.id = self._siguiente_id(datos)
        datos.append(entidad.to_dict())
        JsonManager.escribir(ARCHIVO, datos)
        return entidad

    def listar(self):
        return [Empleado.from_dict(d) for d in JsonManager.leer(ARCHIVO)]

    @log_operacion
    def eliminar(self, id_entidad):
        datos = JsonManager.leer(ARCHIVO)
        nuevos = [d for d in datos if d["id"] != id_entidad]
        if len(nuevos) == len(datos):
            return False
        JsonManager.escribir(ARCHIVO, nuevos)
        return True

    def renumerar_ids(self):
        datos = JsonManager.leer(ARCHIVO)
        mapeo = {}
        for nuevo_id, emp in enumerate(datos, start=1):
            mapeo[emp["id"]] = nuevo_id
            emp["id"] = nuevo_id
        JsonManager.escribir(ARCHIVO, datos)
        return mapeo

    def buscar_por_id(self, id_entidad):
        for d in JsonManager.leer(ARCHIVO):
            if d["id"] == id_entidad:
                return Empleado.from_dict(d)
        return None
