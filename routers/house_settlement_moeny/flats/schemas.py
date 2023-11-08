from pydantic import BaseModel

class AddFlatsParams(BaseModel):
    id_user: str
    username: str
    house_name: str
    professional_house_name: str


    class Config:
        orm_mode: True