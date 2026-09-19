from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from typing import Dict, Set, Optional


class RestauranteServicio:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        usuarios_iniciales: list[Usuario] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        # ========== COLECCIONES PRINCIPALES (se mantienen) ==========
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._usuarios: list[Usuario] = usuarios_iniciales.copy() if usuarios_iniciales else []
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

        # ========== ÍNDICES AUXILIARES — Semana 12 ==========
        # Búsqueda directa por clave → O(1) en lugar de recorrer lista
        self._productos_por_codigo: Dict[str, Producto] = {}
        self._usuarios_por_id: Dict[str, Usuario] = {}

        # Ventas agrupadas por usuario → consulta sin recorrido completo
        self._ventas_por_usuario: Dict[str, list[Venta]] = {}

        # Validaciones rápidas de existencia
        self._codigos_producto: Set[str] = set()
        self._ids_usuario: Set[str] = set()

        # Reconstruir índices desde los datos cargados de JSON
        self._reconstruir_indices()

    # ==============================================================
    # ✅ MÉTODO NUEVO — Reconstruir índices al iniciar
    # ==============================================================
    def _reconstruir_indices(self) -> None:
        """Reconstruye todos los índices desde las listas tras cargar JSON.
        Se llama automáticamente al crear el servicio."""
        # Limpiar índices actuales
        self._productos_por_codigo.clear()
        self._usuarios_por_id.clear()
        self._ventas_por_usuario.clear()
        self._codigos_producto.clear()
        self._ids_usuario.clear()

        # Reconstruir índice de productos
        for producto in self._productos:
            self._productos_por_codigo[producto.codigo] = producto
            self._codigos_producto.add(producto.codigo)

        # Reconstruir índice de usuarios
        for usuario in self._usuarios:
            self._usuarios_por_id[usuario.identificacion] = usuario
            self._ids_usuario.add(usuario.identificacion)

        # Reconstruir agrupación de ventas por usuario
        for venta in self._ventas:
            uid = venta.usuario_id
            if uid not in self._ventas_por_usuario:
                self._ventas_por_usuario[uid] = []
            self._ventas_por_usuario[uid].append(venta)

    # ==============================================================
    # ✅ BÚSQUEDAS MEJORADAS — Ya no recorren toda la lista
    # ==============================================================
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """Antes: recorrido completo → O(n)  |  Ahora: consulta directa → O(1)"""
        codigo = codigo.strip()
        return self._productos_por_codigo.get(codigo)

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """Antes: recorrido completo → O(n)  |  Ahora: consulta directa → O(1)"""
        identificacion = identificacion.strip()
        return self._usuarios_por_id.get(identificacion)

    def consultar_ventas_usuario(self, identificacion: str) -> list[Venta]:
        """Antes: recorrer toda la lista de ventas → O(n)
        Ahora: devolver lista ya agrupada → O(1)"""
        identificacion = identificacion.strip()
        return self._ventas_por_usuario.get(identificacion, [])

    # ==============================================================
    # ✅ REGISTROS — Mantienen índices SINCRONIZADOS
    # ==============================================================
    def registrar_producto(self, producto: Producto) -> bool:
        """Valida con set y mantiene lista + índice actualizados."""
        if producto.codigo in self._codigos_producto:
            return False
        self._productos.append(producto)
        # ✅ Sincronizar índice
        self._productos_por_codigo[producto.codigo] = producto
        self._codigos_producto.add(producto.codigo)
        return True

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Valida con set y mantiene lista + índice actualizados."""
        if usuario.identificacion in self._ids_usuario:
            return False
        self._usuarios.append(usuario)
        # ✅ Sincronizar índice
        self._usuarios_por_id[usuario.identificacion] = usuario
        self._ids_usuario.add(usuario.identificacion)
        return True

    def realizar_venta(self, codigo_producto: str, usuario_id: str, cantidad: int = 1) -> bool:
        """Realiza venta, descuenta stock y mantiene índices sincronizados."""
        # Búsquedas ahora optimizadas
        producto = self.buscar_producto(codigo_producto)
        usuario = self.buscar_usuario(usuario_id)

        if producto is None or usuario is None:
            return False
        if producto.stock < cantidad:
            return False

        # Descontar stock
        producto.vender(cantidad)

        # Registrar venta
        venta = Venta(usuario_id, codigo_producto, cantidad)
        self._ventas.append(venta)

        # ✅ Sincronizar índice de ventas por usuario
        uid = usuario_id.strip()
        if uid not in self._ventas_por_usuario:
            self._ventas_por_usuario[uid] = []
        self._ventas_por_usuario[uid].append(venta)
        return True

    # ==============================================================
    # 📋 MÉTODOS DE CONSULTA — se mantienen o mejorados
    # ==============================================================
    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()