class TipoPermiso:
    def __init__(self, id, descripcion, remunerado):
        self.id = id
        self.descripcion = descripcion
        self.remunerado = remunerado.upper()  # "S" o "N"

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "remunerado": self.remunerado,
        }

    @staticmethod
    def from_dict(d):
        return TipoPermiso(d["id"], d["descripcion"], d["remunerado"])
