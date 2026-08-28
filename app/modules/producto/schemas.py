from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    categoria: str = Field(min_length=2, max_length=50)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    stock_minimo: int = Field(default=5, ge=0)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    categoria: str | None = Field(default=None, min_length=2, max_length=50)
    precio: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)


class ProductoRead(ProductoBase):
    id: int


class ProductoStockResponse(BaseModel):
    id: int
    stock: int
    alerta_reposicion: bool