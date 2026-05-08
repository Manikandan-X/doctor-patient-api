from pydantic import BaseModel, EmailStr, Field


# 🔐 LOGIN REQUEST
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


# 🔑 TOKEN RESPONSE
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 🔁 FORGOT PASSWORD
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# 🔄 RESET PASSWORD
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)