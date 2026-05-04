class Permiso:
    def __init__(self, id, id_empleado, id_tipo_permiso,
                 fecha_desde, fecha_hasta, tipo, tiempo, descuento=0.0):
        self.id = id
        self.id_empleado = id_empleado
        self.id_tipo_permiso = id_tipo_permiso
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.tipo = tipo.upper()      # "D" o "H"
        self.tiempo = float(tiempo)
        self.descuento = float(descuento)

    def to_dict(self):
        return {
            "id": self.id,
            "id_empleado": self.id_empleado,
            "id_tipo_permiso": self.id_tipo_permiso,
            "fecha_desde": self.fecha_desde,
            "fecha_hasta": self.fecha_hasta,
            "tipo": self.tipo,
            "tiempo": self.tiempo,
            "descuento": self.descuento,
        }

    @staticmethod
    def from_dict(d):
        return Permiso(
            d["id"], d["id_empleado"], d["id_tipo_permiso"],
            d["fecha_desde"], d["fecha_hasta"], d["tipo"],
            d["tiempo"], d.get("descuento", 0.0)
        )
