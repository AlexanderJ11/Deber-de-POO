from core import ICrud, JsonManager, log_operacion
from models import Permiso

ARCHIVO = "permisos.json"


class PermisoController(ICrud):

    def _siguiente_id(self, lista):
        return max((e["id"] for e in lista), default=0) + 1

    @log_operacion
    def crear(self, entidad: Permiso):
        datos = JsonManager.leer(ARCHIVO)
        entidad.id = self._siguiente_id(datos)
        datos.append(entidad.to_dict())
        JsonManager.escribir(ARCHIVO, datos)
        return entidad

    def listar(self):
        return [Permiso.from_dict(d) for d in JsonManager.leer(ARCHIVO)]

    @log_operacion
    def eliminar(self, id_entidad):
        datos = JsonManager.leer(ARCHIVO)
        nuevos = [d for d in datos if d["id"] != id_entidad]
        if len(nuevos) == len(datos):
            return False
        JsonManager.escribir(ARCHIVO, nuevos)
        return True

    def actualizar_ids_empleado(self, mapeo):
        datos = JsonManager.leer(ARCHIVO)
        for p in datos:
            if p["id_empleado"] in mapeo:
                p["id_empleado"] = mapeo[p["id_empleado"]]
        JsonManager.escribir(ARCHIVO, datos)

    def actualizar_ids_tipo_permiso(self, mapeo):
        datos = JsonManager.leer(ARCHIVO)
        for p in datos:
            if p["id_tipo_permiso"] in mapeo:
                p["id_tipo_permiso"] = mapeo[p["id_tipo_permiso"]]
        JsonManager.escribir(ARCHIVO, datos)

    def renumerar_ids(self):
        datos = JsonManager.leer(ARCHIVO)
        for nuevo_id, per in enumerate(datos, start=1):
            per["id"] = nuevo_id
        JsonManager.escribir(ARCHIVO, datos)
