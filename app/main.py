from fastapi import FastAPI
from app.modules.producto.routers import router as producto_router

app = FastAPI(
    title="Sistema de Gestión de Stock",
    version="1.0.0",
    description="API REST modular para la administración de inventario.",
)

# Registro del enrutador del módulo de productos
app.include_router(producto_router)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {
        "status": "online",
        "message": "Servicio de gestión de stock operativo",
    }