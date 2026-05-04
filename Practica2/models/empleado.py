class Empleado:
    def __init__(self, id, nombre, cedula, sueldo):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.sueldo = float(sueldo)
        self.valor_hora = round(self.sueldo / 240, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "sueldo": self.sueldo,
            "valor_hora": self.valor_hora,
        }

    @staticmethod
    def from_dict(d):
        return Empleado(d["id"], d["nombre"], d["cedula"], d["sueldo"])
