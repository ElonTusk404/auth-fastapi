import uuid
from src.models import BaseModel
from sqlalchemy import JSON, String, UUID
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    username: Mapped[str] = mapped_column(String(64), nullable=False)

    password: Mapped[str] = mapped_column(String(256), nullable=False)

    scopes: Mapped[list] = mapped_column(JSON, default=[
    "read:products", "write:products", "update:products", "delete:products",
    "read:orders", "write:orders", "update:orders", "delete:orders",
    "read:carts", "write:carts", "update:carts", "delete:carts"
])