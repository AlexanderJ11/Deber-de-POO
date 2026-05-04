from core.mixins import EstadisticasMixin, ImpresionMixin
from core.consola import Color, c


class EstadisticasController(EstadisticasMixin, ImpresionMixin):

    def _fila(self, label, valor, color_valor=Color.BLANCO_B):
        print(f"  {c(label, Color.CIAN):<40} {c(str(valor), color_valor, Color.NEGRITA)}")

    def generar(self, empleados, tipos, permisos):
        rem    = self.permisos_remunerados(permisos, tipos)
        no_rem = self.permisos_no_remunerados(permisos, tipos)
        total_tiempo    = self.total_tiempo(permisos)
        total_descuento = self.sumar(permisos, lambda p: p.descuento)

        self.encabezado("Estadísticas de Permisos")
        print()
        self._fila("Total empleados registrados",    self.contar(empleados),   Color.AZUL_B)
        self._fila("Total permisos registrados",     self.contar(permisos),    Color.AZUL_B)
        self.separador()
        self._fila("Permisos remunerados",           self.contar(rem),         Color.VERDE_B)
        self._fila("Permisos no remunerados",        self.contar(no_rem),      Color.ROJO_B)
        self.separador()
        self._fila("Total tiempo solicitado",        f"{total_tiempo:.2f}",    Color.AMARILLO_B)
        self._fila("Monto total descontado",         f"$ {total_descuento:.2f}", Color.ROJO_B)
        self.separador()
