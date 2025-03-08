from dataclasses import dataclass

from fastapi import Query
from pydantic import UUID4, BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=8, max_length=256)

class CreateUserResponse(BaseModel):
    id: UUID4


