from pydantic import BaseModel, EmailStr, Field

class UserRegisterationInput(BaseModel):
    firstname:str = Field(title="Username", description="The user name that will appear everywhere", min_length=3, max_length=50)
    lastname: str = Field(title="Username", description="The user name that will appear everywhere", min_length=3,max_length=50)
    email:EmailStr
    number:str
    password:bytes = Field(title="User password", description="User password to protect account")
    confirmPassword:bytes = Field(title=" Confirm user password", description="User password to protect account")


class UserLoginInput(BaseModel):
    email:EmailStr
    password:bytes

class GetPasswordResetLink(BaseModel):
    email:EmailStr

class UserPasswordReset(BaseModel):
    email:EmailStr
    passcode:str = Field(max_length=5)
    password:str
    confirmPassword:str





