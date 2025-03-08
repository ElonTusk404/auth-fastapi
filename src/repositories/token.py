from src.models import RefreshTokenModel
from src.utils.repository import SqlAlchemyRepository


class RefreshTokenRepository(SqlAlchemyRepository):
    model = RefreshTokenModel