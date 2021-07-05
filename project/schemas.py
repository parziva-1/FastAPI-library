print("hi")
from pydantic import BaseModel
from pydantic import validator
from typing import Any, Optional
from pydantic.utils import GetterDict
from datetime import datetime

from sqlalchemy.sql.elements import Null


class UserRequesModel(BaseModel):
    email: str
    hashedPassword: str
    dateBirth: datetime
    firstName: str
    secondName: str
    firstSurname: str
    secondSurname: str
    address: str
    number_id: int
    createDate: str

    @validator("email")
    def username_validator(cls, email):
        if len(email) < 3 or len(email) > 50:
            raise ValueError("La longitud mínima es de 3 caracteres y máxima de 50.")

        return email

class UserResponseModel(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True