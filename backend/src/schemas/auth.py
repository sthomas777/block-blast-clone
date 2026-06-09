from pydantic import BaseModel, Field, SecretStr


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: SecretStr = Field(min_length=8)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PlayerResponse(BaseModel):
    player_id: int
    username: str


class AuthSettings(BaseModel):
    secret_key: SecretStr
    access_token_expire_minutes: int = 15
