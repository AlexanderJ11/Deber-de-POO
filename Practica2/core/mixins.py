from .consola import Color, c, gotoxy, limpiar


class EstadisticasMixin:
    """Mixin que provee funciones de orden superior para estadísticas."""

    def contar(self, lista):
        return len(lista)

    def filtrar(self, lista, condicion):
        return list(filter(condicion, lista))

    def sumar(self, lista, clave):
        return sum(map(clave, lista))

    def total_tiempo(self, permisos):
        return self.sumar(permisos, lambda p: p.tiempo)

    def permisos_remunerados(self, permisos, tipos):
        ids = {t.id for t in tipos if t.remunerado == "S"}
        return self.filtrar(permisos, lambda p: p.id_tipo_permiso in ids)

    def permisos_no_remunerados(self, permisos, tipos):
        ids = {t.id for t in tipos if t.remunerado == "N"}
        return self.filtrar(permisos, lambda p: p.id_tipo_permiso in ids)


class ImpresionMixin:
    """Mixin para imprimir cabeceras, separadores y mensajes con color."""

    ANCHO = 44

    def encabezado(self, titulo):
        limpiar()
        borde = c("═" * self.ANCHO, Color.CIAN_B, Color.NEGRITA)
        titulo_fmt = c(f"{titulo.upper():^{self.ANCHO}}", Color.BLANCO_B, Color.NEGRITA)
        print(f"\n{borde}")
        print(titulo_fmt)
        print(borde)

    def separador(self):
        print(c("─" * self.ANCHO, Color.CIAN))

    def mensaje_ok(self, texto):
        print(c(f"\n  ✔  {texto}", Color.VERDE_B, Color.NEGRITA))

    def mensaje_error(self, texto):
        print(c(f"\n  ✘  {texto}", Color.ROJO_B, Color.NEGRITA))

    def etiqueta(self, label, valor):
        """Imprime 'Label : valor' con label en cian y valor en blanco."""
        print(f"  {c(label, Color.CIAN)} : {c(valor, Color.BLANCO_B)}")

    def titulo_seccion(self, texto):
        print(c(f"\n  ▶  {texto}", Color.AMARILLO_B, Color.NEGRITA))
