from abc import ABC, abstractmethod


class ICrud(ABC):
    @abstractmethod
    def crear(self, entidad):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def eliminar(self, id_entidad):
        pass
