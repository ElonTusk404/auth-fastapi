from src.models import BaseModel
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid  

class RefreshTokenModel(BaseModel):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    token: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)

    user_agent: Mapped[str] = mapped_column(String(256), nullable=True)
    
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)