from typing import Optional
from pydantic import BaseModel

    
class UserSignUp(BaseModel):
    login:str
    password:Optional[str]
    name:str
    age:int
    height:int

    class Config:
        orm_mode=True


class UserSignIn(BaseModel):
    login:str
    password:Optional[str]