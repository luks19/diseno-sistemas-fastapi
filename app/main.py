from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Gestión de Stock",
    version="1.0.0",
    description="API REST modular para la administración de inventario.",
)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {
        "status": "online",
        "message": "Servicio de gestión de stock operativo",
    }