# Restaurante App — Semana 12
## Optimización de Rendimiento con Colecciones

**Nombre completo:** Merlinthon Wilfrido España Carbo

**Asignatura:** Programación Orientada a Objetos


### Descripción
Se mantuvo toda la funcionalidad de la Semana 11 sin agregar nuevas entidades. La mejora consiste en **índices auxiliares** que reducen recorridos innecesarios al buscar productos, usuarios y consultar ventas por usuario.

---

### Mejoras Aplicadas

| Estructura | Propósito | Operación Mejorada |
|---|---|---|
| `dict[str, Producto]` | Índice por código de producto | Búsqueda directa → O(1) |
| `dict[str, Usuario]` | Índice por identificación de usuario | Búsqueda directa → O(1) |
| `dict[str, list[Venta]]` | Ventas agrupadas por usuario | Consulta sin recorrido completo → O(1) |
| `set[str]` (códigos) | Validación rápida de códigos duplicados | Comprobar existencia → O(1) |
| `set[str]` (IDs) | Validación rápida de usuarios duplicados | Comprobar existencia → O(1) |

> **Antes:** Cada búsqueda recorría la lista completa → O(n)
> **Ahora:** Se consulta directamente en el índice → O(1)

---

### Estructura del Proyecto
```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```
---

### Funcionamiento
- Las **listas principales** se mantienen para almacenar, recorrer y persistir.
- Los **índices se reconstruyen automáticamente al iniciar** desde JSON mediante `_reconstruir_indices()`.
- Cada operación de registro y venta **mantiene sincronizados** los índices.
- Al guardar, se siguen guardando las listas (los índices NO se guardan, se reconstruyen al cargar).

---

### Ejecución
python main.py

La aplicación carga automáticamente los archivos de datos/, reconstruye los índices en memoria y guarda los cambios tras cada operación.
