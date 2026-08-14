from pydantic import BaseModel, Field, EmailStr

class CreateUserModel(BaseModel):
    name: str = Field()
    email: EmailStr
    password: str = Field(min_length=8)

class LoginUserModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)



