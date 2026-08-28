from app.modules.producto.schemas import (
    ProductoCreate,
    ProductoRead,
    ProductoStockResponse,
    ProductoUpdate,
)

# Estructura de almacenamiento en memoria (simula la tabla de la base de datos)
_db_productos: list[ProductoRead] = []
_id_counter: int = 1


def crear_producto(datos: ProductoCreate) -> ProductoRead:
    """Instancia un nuevo producto, le asigna un ID autoincremental y lo persiste en memoria."""
    global _id_counter
    nuevo_producto = ProductoRead(id=_id_counter, **datos.model_dump())
    _db_productos.append(nuevo_producto)
    _id_counter += 1
    return nuevo_producto


def listar_productos(skip: int = 0, limit: int = 10) -> list[ProductoRead]:
    """Retorna una porción paginada de la lista de productos."""
    return _db_productos[skip : skip + limit]


def obtener_producto_por_id(producto_id: int) -> ProductoRead | None:
    """Busca un producto por su clave primaria. Retorna None si no existe."""
    for prod in _db_productos:
        if prod.id == producto_id:
            return prod
    return None


def actualizar_producto(
    producto_id: int, datos: ProductoUpdate
) -> ProductoRead | None:
    """Actualiza parcialmente los campos provistos de un producto existente."""
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return None

    # exclude_unset=True ignora los campos que el cliente no envió (evita sobreescribir con None)
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizados.items():
        setattr(producto, clave, valor)

    return producto


def verificar_alerta_stock(producto_id: int) -> ProductoStockResponse | None:
    """Aplica la regla de dominio para determinar si el stock cayó por debajo o igual al mínimo."""
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return None

    necesita_reposicion = producto.stock <= producto.stock_minimo
    return ProductoStockResponse(
        id=producto.id,
        stock=producto.stock,
        alerta_reposicion=necesita_reposicion,
    )