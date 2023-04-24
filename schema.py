import pydantic


class CreateUser(pydantic.BaseModel):
    
    username: str
    password: str
    email: str
    
    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value