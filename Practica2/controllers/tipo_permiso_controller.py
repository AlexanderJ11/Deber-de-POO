from core import ICrud, JsonManager, log_operacion
from models import TipoPermiso

ARCHIVO = "tipos_permiso.json"


class TipoPermisoController(ICrud):

    def _siguiente_id(self, lista):
        return max((e["id"] for e in lista), default=0) + 1

    @log_operacion
    def crear(self, entidad: TipoPermiso):
        datos = JsonManager.leer(ARCHIVO)
        entidad.id = self._siguiente_id(datos)
        datos.append(entidad.to_dict())
        JsonManager.escribir(ARCHIVO, datos)
        return entidad

    def listar(self):
        return [TipoPermiso.from_dict(d) for d in JsonManager.leer(ARCHIVO)]

    @log_operacion
    def eliminar(self, id_entidad):
        datos = JsonManager.leer(ARCHIVO)
        nuevos = [d for d in datos if d["id"] != id_entidad]
        if len(nuevos) == len(datos):
            return False
        JsonManager.escribir(ARCHIVO, nuevos)
        return True

    def buscar_por_id(self, id_entidad):
        for d in JsonManager.leer(ARCHIVO):
            if d["id"] == id_entidad:
                return TipoPermiso.from_dict(d)
        return None

    def renumerar_ids(self):
        datos = JsonManager.leer(ARCHIVO)
        mapeo = {}
        for nuevo_id, tp in enumerate(datos, start=1):
            mapeo[tp["id"]] = nuevo_id
            tp["id"] = nuevo_id
        JsonManager.escribir(ARCHIVO, datos)
        return mapeo
