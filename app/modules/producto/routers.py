from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status

from app.modules.producto import services
from app.modules.producto.schemas import (
    ProductoCreate,
    ProductoRead,
    ProductoStockResponse,
    ProductoUpdate,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post(
    "/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED
)
async def crear_producto(producto: ProductoCreate) -> ProductoRead:
    """Endpoint para registrar un nuevo producto en el inventario."""
    return services.crear_producto(producto)


@router.get("/", response_model=list[ProductoRead], status_code=status.HTTP_200_OK)
async def listar_productos(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
) -> list[ProductoRead]:
    """Endpoint para obtener la lista paginada de productos."""
    return services.listar_productos(skip=skip, limit=limit)


@router.get(
    "/{producto_id}",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
)
async def obtener_producto(
    producto_id: Annotated[int, Path(gt=0)]
) -> ProductoRead:
    """Endpoint para obtener un producto específico mediante su ID."""
    producto = services.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )
    return producto


@router.put(
    "/{producto_id}",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
)
async def actualizar_producto(
    producto_id: Annotated[int, Path(gt=0)],
    datos: ProductoUpdate,
) -> ProductoRead:
    """Endpoint para actualizar parcialmente los atributos de un producto."""
    producto = services.actualizar_producto(producto_id, datos)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )
    return producto


@router.get(
    "/{producto_id}/alerta-stock",
    response_model=ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
async def consultar_alerta_stock(
    producto_id: Annotated[int, Path(gt=0)]
) -> ProductoStockResponse:
    """Endpoint para evaluar si un producto requiere reposición según su stock actual y mínimo."""
    alerta = services.verificar_alerta_stock(producto_id)
    if not alerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )
    return alerta