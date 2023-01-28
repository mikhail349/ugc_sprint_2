from typing import List

from pydantic import Field, Required

from src.configs.base import BaseConfig


class JWTConfig(BaseConfig):
    """Настройки JWT."""
    jwt_token_location: List[str] = ["headers"]
    """Секция запроса с токеном."""
    jwt_access_token_expires: int = Field(3600, env="JWT_ACCESS_TOKEN_EXPIRES")
    """Срок жизни access-токена (секунд)."""
    jwt_algorithm: str = Field("RS256", env="JWT_ALGORITHM")
    """Алгоритм JWT."""
    jwt_public_key_path: str = Field(Required, env="JWT_PUBLIC_KEY_PATH")
    """Путь до публичного ключа."""


jwt_config = JWTConfig()
