import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from core.decorators import validar_entrada
from core.mixins import ImpresionMixin
from core.consola import Color, c, limpiar, gotoxy, pausa, ansi_ljust, fila
from controllers import (
    EmpleadoController, TipoPermisoController,
    PermisoController, EstadisticasController
)
from models import Empleado, TipoPermiso, Permiso


# ══════════════════════════════════════════════
#  VALIDACIONES
# ══════════════════════════════════════════════

def validar_cedula_ecuatoriana(cedula: str) -> bool:
    if not cedula.isdigit() or len(cedula) != 10:
        return False
    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False
    if int(cedula[2]) >= 6:
        return False
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i, coef in enumerate(coeficientes):
        val = int(cedula[i]) * coef
        if val >= 10:
            val -= 9
        total += val
    return (10 - total % 10) % 10 == int(cedula[9])


CANCELAR_MSG = c("  (escriba 'cancelar' en cualquier campo para cancelar)", Color.MAGENTA_B)

# S/N acepta: S, SI, SÍ, SÍ, YES  /  N, NO
_SI  = {"s", "si", "sí", "si", "yes"}
_NO  = {"n", "no"}

def pedir_texto(prompt, min_len=2, solo_letras=False):
    while True:
        valor = input(c(prompt, Color.AMARILLO)).strip()
        if valor.lower() == "cancelar":
            return None
        if solo_letras:
            if len(valor) >= min_len and re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+", valor):
                return valor
            print(c(f"  ⚠  Solo se permiten letras (mínimo {min_len} caracteres, sin números ni símbolos).", Color.ROJO_B))
        else:
            if len(valor) >= min_len and not valor.isdigit():
                return valor
            print(c(f"  ⚠  Ingrese texto válido (mínimo {min_len} caracteres).", Color.ROJO_B))


def pedir_numero(prompt, positivo=True, entero=False):
    while True:
        raw = input(c(prompt, Color.AMARILLO)).strip()
        if raw.lower() == "cancelar":
            return None
        try:
            valor = float(raw)
            if positivo and valor <= 0:
                raise ValueError("Debe ser mayor a 0.")
            return int(valor) if entero else round(valor, 2)
        except ValueError as e:
            print(c(f"  ⚠  {e} Intente de nuevo.", Color.ROJO_B))


def pedir_fecha(prompt):
    while True:
        texto = input(c(prompt, Color.AMARILLO)).strip()
        if texto.lower() == "cancelar":
            return None
        try:
            datetime.strptime(texto, "%Y-%m-%d")
            return texto
        except ValueError:
            print(c("  ⚠  Formato incorrecto. Use YYYY-MM-DD (ej: 2024-05-01).", Color.ROJO_B))


def pedir_opcion_sn(prompt):
    """Acepta: S, Si, Sí, SI / N, No, NO — y 'cancelar'."""
    while True:
        val = input(c(prompt, Color.AMARILLO)).strip().lower()
        if val == "cancelar":
            return None
        if val in _SI:
            return "S"
        if val in _NO:
            return "N"
        print(c("  ⚠  Ingrese S, Si, Sí / N o No.", Color.ROJO_B))


def pedir_tipo_dh(prompt):
    """Acepta D, Dia, Días / H, Hora, Horas — y 'cancelar'."""
    DIAS  = {"d", "dia", "dias", "días", "día"}
    HORAS = {"h", "hora", "horas"}
    while True:
        val = input(c(prompt, Color.AMARILLO)).strip().lower()
        if val == "cancelar":
            return None
        if val in DIAS:
            return "D"
        if val in HORAS:
            return "H"
        print(c("  ⚠  Ingrese D, Días / H u Horas.", Color.ROJO_B))


def _cancelado():
    mixin.mensaje_error("Operación cancelada.")
    pausa()


# ══════════════════════════════════════════════
#  CONTROLADORES
# ══════════════════════════════════════════════

mixin             = ImpresionMixin()
ctrl_empleado     = EmpleadoController()
ctrl_tipo_permiso = TipoPermisoController()
ctrl_permiso      = PermisoController()
ctrl_estadisticas = EstadisticasController()


# ══════════════════════════════════════════════
#  MÓDULO: EMPLEADO
# ══════════════════════════════════════════════

@validar_entrada
def registrar_empleado():
    mixin.encabezado("Registro de Empleado")
    gotoxy(2, 5)
    print(c("  ID: [GENERADO AUTOMÁTICAMENTE]", Color.MAGENTA_B))
    print(CANCELAR_MSG + "\n")

    nombre = pedir_texto("  Nombre       : ", solo_letras=True)
    if nombre is None: return _cancelado()

    sueldo = pedir_numero("  Sueldo       : $ ")
    if sueldo is None: return _cancelado()

    while True:
        cedula = input(c("  Cédula       : ", Color.AMARILLO)).strip()
        if cedula.lower() == "cancelar": return _cancelado()
        if not validar_cedula_ecuatoriana(cedula):
            print(c("  ⚠  Cédula ecuatoriana inválida. Verifique los 10 dígitos.", Color.ROJO_B))
            continue
        if any(e.cedula == cedula for e in ctrl_empleado.listar()):
            print(c("  ⚠  Ya existe un empleado registrado con esa cédula.", Color.ROJO_B))
            continue
        break

    valor_hora = round(sueldo / 240, 2)
    mixin.separador()
    print(c(f"  Valor hora calculado : $ {valor_hora:.2f}", Color.VERDE_B))
    mixin.separador()

    confirm = pedir_opcion_sn("  ¿Desea guardar? (S/N): ")
    if confirm is None or confirm == "N": return _cancelado()

    emp = Empleado(None, nombre, cedula, sueldo)
    ctrl_empleado.crear(emp)
    mixin.mensaje_ok(f"Empleado '{nombre}' guardado con ID {emp.id}.")
    pausa()


@validar_entrada
def listar_empleados(con_pausa=True):
    mixin.encabezado("Lista de Empleados")
    lista = ctrl_empleado.listar()
    if not lista:
        print(c("  No hay empleados registrados.", Color.AMARILLO_B))
        if con_pausa: pausa()
        return
    gotoxy(2, 5)
    # Cabecera
    fila(
        (c("ID",      Color.CIAN_B), 8),
        (c("Nombre",  Color.CIAN_B), 30),
        (c("Cédula",  Color.CIAN_B), 14),
        (c("Sueldo",  Color.CIAN_B), 12),
        (c("V/Hora",  Color.CIAN_B), 10),
    )
    mixin.separador()
    for e in lista:
        fila(
            (c(f"[{e.id}]",        Color.MAGENTA_B), 8),
            (e.nombre,                                30),
            (e.cedula,                                14),
            (f"$ {e.sueldo:.2f}",                     12),
            (c(f"$ {e.valor_hora:.2f}", Color.VERDE_B), 10),
        )
    mixin.separador()
    if con_pausa: pausa()


@validar_entrada
def eliminar_empleado():
    listar_empleados(con_pausa=False)
    mixin.titulo_seccion("Eliminar Empleado")
    print(c("  ⚠  También se eliminarán todos los permisos asociados.", Color.AMARILLO_B))
    print(CANCELAR_MSG)

    id_emp = pedir_numero("  ID a eliminar: ", entero=True)
    if id_emp is None: return _cancelado()

    empleado = ctrl_empleado.buscar_por_id(id_emp)
    if not empleado:
        mixin.mensaje_error("ID no encontrado.")
        pausa()
        return

    confirm = pedir_opcion_sn(f"  ¿Eliminar a '{empleado.nombre}' y sus permisos? (S/N): ")
    if confirm is None or confirm == "N": return _cancelado()

    permisos = ctrl_permiso.listar()
    eliminados = sum(1 for p in permisos if p.id_empleado == id_emp and ctrl_permiso.eliminar(p.id))
    ctrl_empleado.eliminar(id_emp)
    mapeo = ctrl_empleado.renumerar_ids()
    ctrl_permiso.actualizar_ids_empleado(mapeo)
    mixin.mensaje_ok(f"Empleado eliminado junto con {eliminados} permiso(s) asociado(s).")
    pausa()


# ══════════════════════════════════════════════
#  MÓDULO: TIPO DE PERMISO
# ══════════════════════════════════════════════

@validar_entrada
def registrar_tipo_permiso():
    mixin.encabezado("Tipo de Permiso")
    gotoxy(2, 5)
    print(c("  ID: [GENERADO AUTOMÁTICAMENTE]", Color.MAGENTA_B))
    print(CANCELAR_MSG + "\n")

    descripcion = pedir_texto("  Descripción          : ")
    if descripcion is None: return _cancelado()

    remunerado = pedir_opcion_sn("  ¿Remunerado? (S/N)   : ")
    if remunerado is None: return _cancelado()

    mixin.separador()
    confirm = pedir_opcion_sn("  ¿Guardar? (S/N): ")
    if confirm is None or confirm == "N": return _cancelado()

    tp = TipoPermiso(None, descripcion, remunerado)
    ctrl_tipo_permiso.crear(tp)
    mixin.mensaje_ok(f"Tipo '{descripcion}' guardado con ID {tp.id}.")
    pausa()


@validar_entrada
def listar_tipos_permiso(con_pausa=True):
    mixin.encabezado("Tipos de Permiso")
    lista = ctrl_tipo_permiso.listar()
    if not lista:
        print(c("  No hay tipos de permiso registrados.", Color.AMARILLO_B))
        if con_pausa: pausa()
        return
    gotoxy(2, 5)
    fila(
        (c("ID",          Color.CIAN_B), 8),
        (c("Descripción", Color.CIAN_B), 34),
        (c("Remunerado",  Color.CIAN_B), 12),
    )
    mixin.separador()
    for t in lista:
        rem_txt = c("Sí ✔", Color.VERDE_B) if t.remunerado == "S" else c("No ✘", Color.ROJO_B)
        fila(
            (c(f"[{t.id}]",  Color.MAGENTA_B), 8),
            (t.descripcion,                     34),
            (rem_txt,                            12),
        )
    mixin.separador()
    if con_pausa: pausa()


@validar_entrada
def eliminar_tipo_permiso():
    listar_tipos_permiso(con_pausa=False)
    mixin.titulo_seccion("Eliminar Tipo de Permiso")
    print(c("  ⚠  También se eliminarán todos los permisos que usen este tipo.", Color.AMARILLO_B))
    print(CANCELAR_MSG)

    id_tipo = pedir_numero("  ID a eliminar: ", entero=True)
    if id_tipo is None: return _cancelado()

    tipo = ctrl_tipo_permiso.buscar_por_id(id_tipo)
    if not tipo:
        mixin.mensaje_error("ID no encontrado.")
        pausa()
        return

    confirm = pedir_opcion_sn(f"  ¿Eliminar tipo '{tipo.descripcion}' y sus permisos? (S/N): ")
    if confirm is None or confirm == "N": return _cancelado()

    permisos = ctrl_permiso.listar()
    eliminados = sum(1 for p in permisos if p.id_tipo_permiso == id_tipo and ctrl_permiso.eliminar(p.id))
    ctrl_tipo_permiso.eliminar(id_tipo)
    mapeo = ctrl_tipo_permiso.renumerar_ids()
    ctrl_permiso.actualizar_ids_tipo_permiso(mapeo)
    ctrl_permiso.renumerar_ids()
    mixin.mensaje_ok(f"Tipo eliminado junto con {eliminados} permiso(s) asociado(s).")
    pausa()


# ══════════════════════════════════════════════
#  MÓDULO: PERMISO
# ══════════════════════════════════════════════

@validar_entrada
def registrar_permiso():
    mixin.encabezado("Registro de Permiso")
    gotoxy(2, 5)
    print(c("  ID: [GENERADO AUTOMÁTICAMENTE]", Color.MAGENTA_B))
    print(CANCELAR_MSG + "\n")

    listar_empleados(con_pausa=False)
    id_emp = pedir_numero("  ID Empleado      : ", entero=True)
    if id_emp is None: return _cancelado()
    empleado = ctrl_empleado.buscar_por_id(id_emp)
    if not empleado:
        mixin.mensaje_error("Empleado no encontrado.")
        pausa()
        return

    listar_tipos_permiso(con_pausa=False)
    id_tipo = pedir_numero("  ID Tipo Permiso  : ", entero=True)
    if id_tipo is None: return _cancelado()
    tipo_permiso = ctrl_tipo_permiso.buscar_por_id(id_tipo)
    if not tipo_permiso:
        mixin.mensaje_error("Tipo de permiso no encontrado.")
        pausa()
        return

    fecha_desde = pedir_fecha("  Fecha desde      : ")
    if fecha_desde is None: return _cancelado()

    fecha_hasta = pedir_fecha("  Fecha hasta      : ")
    if fecha_hasta is None: return _cancelado()

    while datetime.strptime(fecha_hasta, "%Y-%m-%d") < datetime.strptime(fecha_desde, "%Y-%m-%d"):
        print(c("  ⚠  Fecha hasta debe ser igual o posterior a fecha desde.", Color.ROJO_B))
        fecha_hasta = pedir_fecha("  Fecha hasta      : ")
        if fecha_hasta is None: return _cancelado()

    tipo = pedir_tipo_dh("  Tipo (D/Días | H/Horas): ")
    if tipo is None: return _cancelado()

    tiempo = pedir_numero("  Tiempo (cantidad): ")
    if tiempo is None: return _cancelado()

    descuento = 0.0
    if tipo_permiso.remunerado == "N":
        descuento = round(empleado.valor_hora * (tiempo if tipo == "H" else tiempo * 8), 2)

    mixin.separador()
    rem_txt = c("Sí", Color.VERDE_B) if tipo_permiso.remunerado == "S" else c("No", Color.ROJO_B)
    fila((c("Empleado",          Color.CIAN), 24), (empleado.nombre,          30))
    fila((c("Tipo de permiso",   Color.CIAN), 24), (tipo_permiso.descripcion, 30))
    fila((c("¿Remunerado?",      Color.CIAN), 24), (rem_txt,                  10))
    fila((c("Descuento aplicado",Color.CIAN), 24), (c(f"$ {descuento:.2f}", Color.AMARILLO_B), 10))
    mixin.separador()

    confirm = pedir_opcion_sn("  ¿Confirmar? (S/N): ")
    if confirm is None or confirm == "N": return _cancelado()

    per = Permiso(None, id_emp, id_tipo, fecha_desde, fecha_hasta, tipo, tiempo, descuento)
    ctrl_permiso.crear(per)
    mixin.mensaje_ok(f"Permiso registrado con ID {per.id}.")
    pausa()


@validar_entrada
def listar_permisos(con_pausa=True):
    mixin.encabezado("Lista de Permisos")
    permisos = ctrl_permiso.listar()
    if not permisos:
        print(c("  No hay permisos registrados.", Color.AMARILLO_B))
        if con_pausa: pausa()
        return

    empleados = {e.id: e.nombre for e in ctrl_empleado.listar()}
    tipos     = {t.id: t.descripcion for t in ctrl_tipo_permiso.listar()}

    gotoxy(2, 5)
    fila(
        (c("ID",          Color.CIAN_B),  6),
        (c("Empleado",    Color.CIAN_B), 28),
        (c("Tipo Permiso",Color.CIAN_B), 22),
        (c("Desde",       Color.CIAN_B), 13),
        (c("Hasta",       Color.CIAN_B), 13),
        (c("Tipo",        Color.CIAN_B),  8),
        (c("Tiempo",      Color.CIAN_B),  8),
        (c("Descuento",   Color.CIAN_B), 10),
    )
    mixin.separador()
    for p in permisos:
        nom_emp  = empleados.get(p.id_empleado,    f"ID:{p.id_empleado}")
        nom_tipo = tipos.get(p.id_tipo_permiso,     f"ID:{p.id_tipo_permiso}")
        tipo_txt = c("Días",  Color.AZUL_B) if p.tipo == "D" else c("Horas", Color.AZUL_B)
        fila(
            (c(f"[{p.id}]",             Color.MAGENTA_B),  6),
            (nom_emp,                                       28),
            (nom_tipo,                                      22),
            (p.fecha_desde,                                 13),
            (p.fecha_hasta,                                 13),
            (tipo_txt,                                       8),
            (str(p.tiempo),                                  8),
            (c(f"$ {p.descuento:.2f}",  Color.AMARILLO_B), 10),
        )
    mixin.separador()
    if con_pausa: pausa()


@validar_entrada
def eliminar_permiso():
    listar_permisos(con_pausa=False)
    mixin.titulo_seccion("Eliminar Permiso")
    print(CANCELAR_MSG)

    id_per = pedir_numero("  ID a eliminar: ", entero=True)
    if id_per is None: return _cancelado()

    permiso = next((p for p in ctrl_permiso.listar() if p.id == id_per), None)
    if not permiso:
        mixin.mensaje_error("ID no encontrado.")
        pausa()
        return

    empleados = {e.id: e.nombre for e in ctrl_empleado.listar()}
    tipos     = {t.id: t.descripcion for t in ctrl_tipo_permiso.listar()}
    nom_emp  = empleados.get(permiso.id_empleado,  "?")
    nom_tipo = tipos.get(permiso.id_tipo_permiso,  "?")

    confirm = pedir_opcion_sn(f"  ¿Eliminar permiso de '{nom_emp}' / '{nom_tipo}'? (S/N): ")
    if confirm is None or confirm == "N": return _cancelado()

    ctrl_permiso.eliminar(id_per)
    ctrl_permiso.renumerar_ids()
    mixin.mensaje_ok("Permiso eliminado correctamente.")
    pausa()


# ══════════════════════════════════════════════
#  MÓDULO: ESTADÍSTICAS
# ══════════════════════════════════════════════

def ver_estadisticas():
    ctrl_estadisticas.generar(
        ctrl_empleado.listar(),
        ctrl_tipo_permiso.listar(),
        ctrl_permiso.listar()
    )
    pausa()


# ══════════════════════════════════════════════
#  SUB-MENÚS
# ══════════════════════════════════════════════

def _opcion(num, texto):
    print(f"  {c(f'[{num}]', Color.CIAN_B, Color.NEGRITA)} {c(texto, Color.BLANCO_B)}")


def menu_empleado():
    while True:
        mixin.encabezado("Módulo — Empleados")
        gotoxy(2, 5)
        _opcion(1, "Registrar empleado")
        _opcion(2, "Consultar empleados")
        _opcion(3, "Eliminar empleado")
        _opcion(0, "Volver al menú principal")
        mixin.separador()
        op = input(c("  Opción: ", Color.AMARILLO_B)).strip()
        if   op == "1": registrar_empleado()
        elif op == "2": listar_empleados()
        elif op == "3": eliminar_empleado()
        elif op == "0": break
        else: mixin.mensaje_error("Opción no válida."); pausa()


def menu_tipo_permiso():
    while True:
        mixin.encabezado("Módulo — Tipos de Permiso")
        gotoxy(2, 5)
        _opcion(1, "Registrar tipo de permiso")
        _opcion(2, "Consultar tipos de permiso")
        _opcion(3, "Eliminar tipo de permiso")
        _opcion(0, "Volver al menú principal")
        mixin.separador()
        op = input(c("  Opción: ", Color.AMARILLO_B)).strip()
        if   op == "1": registrar_tipo_permiso()
        elif op == "2": listar_tipos_permiso()
        elif op == "3": eliminar_tipo_permiso()
        elif op == "0": break
        else: mixin.mensaje_error("Opción no válida."); pausa()


def menu_permiso():
    while True:
        mixin.encabezado("Módulo — Permisos")
        gotoxy(2, 5)
        _opcion(1, "Registrar permiso")
        _opcion(2, "Consultar permisos")
        _opcion(3, "Eliminar permiso")
        _opcion(0, "Volver al menú principal")
        mixin.separador()
        op = input(c("  Opción: ", Color.AMARILLO_B)).strip()
        if   op == "1": registrar_permiso()
        elif op == "2": listar_permisos()
        elif op == "3": eliminar_permiso()
        elif op == "0": break
        else: mixin.mensaje_error("Opción no válida."); pausa()


# ══════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════

def menu_principal():
    while True:
        mixin.encabezado("Sistema de Permisos del Personal")
        gotoxy(2, 5)
        _opcion(1, "Empleados")
        _opcion(2, "Tipos de Permiso")
        _opcion(3, "Permisos")
        _opcion(4, "Estadísticas")
        _opcion(0, "Salir")
        mixin.separador()
        op = input(c("  Opción: ", Color.AMARILLO_B)).strip()
        if   op == "1": menu_empleado()
        elif op == "2": menu_tipo_permiso()
        elif op == "3": menu_permiso()
        elif op == "4": ver_estadisticas()
        elif op == "0":
            limpiar()
            print(c("\n  ¡Hasta luego!\n", Color.VERDE_B, Color.NEGRITA))
            break
        else: mixin.mensaje_error("Opción no válida."); pausa()
