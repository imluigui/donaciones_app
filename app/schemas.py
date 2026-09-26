from pydantic import BaseModel, EmailStr
from typing import Optional

class DonanteBase(BaseModel):
    email: EmailStr
    nombre: str

class DonanteCreate(DonanteBase):
    password: str

class Donante(DonanteBase):
    id: int
    rol: str = "usuario"

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
