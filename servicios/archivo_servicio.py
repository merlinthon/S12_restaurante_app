import json
from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    def __init__(self, ruta_datos: str = "datos") -> None:
        self._ruta_datos = Path(ruta_datos)
        self._ruta_productos = self._ruta_datos / "productos.json"
        self._ruta_usuarios = self._ruta_datos / "usuarios.json"
        self._ruta_ventas = self._ruta_datos / "ventas.json"

    def cargar_productos(self) -> list[Producto]:
        datos = self._leer_lista(self._ruta_productos, "productos")
        productos: list[Producto] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Registro de producto con formato inválido omitido.")
                continue
            try:
                productos.append(Producto(
                    item["codigo"],
                    item["nombre"],
                    item["precio"],
                    item.get("stock", 0),
                ))
            except KeyError:
                print("Registro de producto incompleto omitido.")
            except ValueError as error:
                print(f"Producto con datos inválidos: {error}")
        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        datos = [p.convertir_a_diccionario() for p in productos]
        return self._guardar_lista(self._ruta_productos, datos, "productos")

    def cargar_usuarios(self) -> list[Usuario]:
        datos = self._leer_lista(self._ruta_usuarios, "usuarios")
        usuarios: list[Usuario] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Registro de usuario con formato inválido omitido.")
                continue
            try:
                usuarios.append(Usuario(item["identificacion"], item["nombre"]))
            except KeyError:
                print("Registro de usuario incompleto omitido.")
            except ValueError as error:
                print(f"Usuario con datos inválidos: {error}")
        return usuarios

    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        datos = [u.convertir_a_diccionario() for u in usuarios]
        return self._guardar_lista(self._ruta_usuarios, datos, "usuarios")

    def cargar_ventas(self) -> list[Venta]:
        datos = self._leer_lista(self._ruta_ventas, "ventas")
        ventas: list[Venta] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Registro de venta con formato inválido omitido.")
                continue
            try:
                ventas.append(Venta(
                    item["usuario_id"],
                    item["producto_codigo"],
                    item.get("cantidad", 1),
                ))
            except KeyError:
                print("Registro de venta incompleto omitido.")
            except ValueError as error:
                print(f"Venta con datos inválidos: {error}")
        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        datos = [v.convertir_a_diccionario() for v in ventas]
        return self._guardar_lista(self._ruta_ventas, datos, "ventas")

    def _leer_lista(self, ruta: Path, nombre: str) -> list:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"El archivo de {nombre} no tiene formato JSON válido.")
            return []
        except PermissionError:
            print(f"Sin permisos para leer {nombre}.")
            return []
        if not isinstance(datos, list):
            print(f"El archivo de {nombre} debe contener una lista.")
            return []
        return datos

    def _guardar_lista(self, ruta: Path, datos: list, nombre: str) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Sin permisos para guardar {nombre}.")
            return False