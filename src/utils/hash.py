from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Получить хэш пароля
    :param password: Строка с паролем
    :return: Хэшированный пароль
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверить, совпадает ли введенный пароль с хэшированным
    :param plain_password: Введенный пароль
    :param hashed_password: Хэшированный пароль
    :return: True, если пароли совпадают, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)