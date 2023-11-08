from pydantic import BaseModel


class ListProductsParams(BaseModel):
    id: str | None = None
    id_user: str
    username: str
    name: str
    amount: int
    model: str
    type: bool

    class Config:
        orm_mode: True


class DeleteProduct(BaseModel):
    id: str | None = None
    id_user: str
    username: str

    class Config:
        orm_mode: True
