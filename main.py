from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import RestauranteServicio


OPCIONES_MENU = (
    ("1", "Registrar producto"),
    ("2", "Buscar producto por código"),
    ("3", "Listar productos"),
    ("4", "Registrar usuario"),
    ("5", "Buscar usuario por identificación"),
    ("6", "Listar usuarios"),
    ("7", "Realizar venta"),
    ("8", "Consultar ventas de usuario"),
    ("9", "Listar todas las ventas"),
    ("0", "Salir"),
)


def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def pedir_entero(mensaje: str, defecto=None) -> int:
    entrada = pedir_texto(mensaje)
    if entrada == "" and defecto is not None:
        return defecto
    return int(entrada)


def pedir_flotante(mensaje: str) -> float:
    return float(pedir_texto(mensaje))


def mostrar_menu() -> None:
    print("\n===== RESTAURANTE APP — Semana 12 =====")
    for numero, desc in OPCIONES_MENU:
        print(f"{numero}. {desc}")


def guardar_todo(archivo_servicio: ArchivoServicio, restaurante: RestauranteServicio) -> None:
    archivo_servicio.guardar_productos(restaurante.listar_productos())
    archivo_servicio.guardar_usuarios(restaurante.listar_usuarios())
    archivo_servicio.guardar_ventas(restaurante.listar_ventas())


def registrar_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio):
    print("\n--- Registrar Producto ---")
    codigo = pedir_texto("Código: ")
    nombre = pedir_texto("Nombre: ")
    precio = pedir_flotante("Precio: ")
    stock = pedir_entero("Stock inicial: ")
    try:
        producto = Producto(codigo, nombre, precio, stock)
        if restaurante.registrar_producto(producto):
            print("✅ Producto registrado.")
            guardar_todo(archivo_servicio, restaurante)
        else:
            print("❌ El código ya existe.")
    except ValueError as e:
        print(f"❌ {e}")


def buscar_producto(restaurante: RestauranteServicio):
    print("\n--- Buscar Producto ---")
    codigo = pedir_texto("Código: ")
    prod = restaurante.buscar_producto(codigo)
    print(prod if prod else "❌ Producto no encontrado.")


def listar_productos(restaurante: RestauranteServicio):
    print("\n--- Lista de Productos ---")
    prods = restaurante.listar_productos()
    if not prods:
        print("Sin productos registrados.")
        return
    for p in prods:
        print(p)


def registrar_usuario(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio):
    print("\n--- Registrar Usuario ---")
    identificacion = pedir_texto("Identificación: ")
    nombre = pedir_texto("Nombre: ")
    try:
        usuario = Usuario(identificacion, nombre)
        if restaurante.registrar_usuario(usuario):
            print("✅ Usuario registrado.")
            guardar_todo(archivo_servicio, restaurante)
        else:
            print("❌ La identificación ya existe.")
    except ValueError as e:
        print(f"❌ {e}")


def buscar_usuario(restaurante: RestauranteServicio):
    print("\n--- Buscar Usuario ---")
    identificacion = pedir_texto("Identificación: ")
    usu = restaurante.buscar_usuario(identificacion)
    print(usu if usu else "❌ Usuario no encontrado.")


def listar_usuarios(restaurante: RestauranteServicio):
    print("\n--- Lista de Usuarios ---")
    usus = restaurante.listar_usuarios()
    if not usus:
        print("Sin usuarios registrados.")
        return
    for u in usus:
        print(u)


def realizar_venta(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio):
    print("\n--- Realizar Venta ---")
    codigo_prod = pedir_texto("Código del producto: ")
    id_usuario = pedir_texto("Identificación del usuario: ")
    cantidad = pedir_entero("Cantidad: ")
    if restaurante.realizar_venta(codigo_prod, id_usuario, cantidad):
        print("✅ Venta realizada.")
        guardar_todo(archivo_servicio, restaurante)
    else:
        print("❌ No se pudo realizar. Verifique datos y stock.")


def consultar_ventas_usuario(restaurante: RestauranteServicio):
    print("\n--- Ventas por Usuario ---")
    id_usuario = pedir_texto("Identificación del usuario: ")
    usuario = restaurante.buscar_usuario(id_usuario)
    if not usuario:
        print("❌ Usuario no encontrado.")
        return
    ventas = restaurante.consultar_ventas_usuario(id_usuario)
    print(f"\n📋 Ventas de {usuario.nombre}:")
    if not ventas:
        print("- Sin ventas registradas.")
        return
    for v in ventas:
        prod = restaurante.buscar_producto(v.producto_codigo)
        nom = prod.nombre if prod else "Desconocido"
        print(f"- {v.producto_codigo} | {nom} | Cantidad: {v.cantidad}")


def listar_ventas(restaurante: RestauranteServicio):
    print("\n--- Historial de Ventas ---")
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("Sin ventas registradas.")
        return
    for v in ventas:
        print(v)


def ejecutar():
    ruta = Path(__file__).resolve().parent / "datos"
    archivo_servicio = ArchivoServicio(str(ruta))

    # Cargar desde JSON y reconstruir índices automáticamente
    restaurante = RestauranteServicio(
        archivo_servicio.cargar_productos(),
        archivo_servicio.cargar_usuarios(),
        archivo_servicio.cargar_ventas(),
    )

    print("✅ Datos cargados. Índices reconstruidos.")

    opciones = {
        "1": lambda: registrar_producto(restaurante, archivo_servicio),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: listar_productos(restaurante),
        "4": lambda: registrar_usuario(restaurante, archivo_servicio),
        "5": lambda: buscar_usuario(restaurante),
        "6": lambda: listar_usuarios(restaurante),
        "7": lambda: realizar_venta(restaurante, archivo_servicio),
        "8": lambda: consultar_ventas_usuario(restaurante),
        "9": lambda: listar_ventas(restaurante),
    }

    while True:
        mostrar_menu()
        op = pedir_texto("Seleccione opción: ")
        if op == "0":
            print("👋 ¡Hasta luego!")
            break
        accion = opciones.get(op)
        if accion:
            accion()
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    ejecutar()