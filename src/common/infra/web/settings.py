from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Paramètres de l'application

    Args:
        BaseSettings (BaseSettings): Paramètres de l'application
    """

    # general
    APP_NAME: str = Field(default="iasimov", description="Nom de l'application")
    APP_VERSION: str = Field(default="0.0.1", description="Version de l'application")

    # server
    HOST: str = Field(default="127.0.0.1", description="Adresse du serveur")
    PORT: int = Field(default=5000, description="Port du serveur")
    SERVER_URL: str = Field(
        default="http://127.0.0.1:5000", description="URL du serveur"
    )

    # database
    DATABASE_URL: str = Field(
        default="sqlite:///./test.db", description="URL de la base de données"
    )
    DATABASE_ECHO: bool = Field(default=True, description="Activer les logs SQL")
    DATABASE_POOL_SIZE: int = Field(
        default=5, description="Nombre maximal de connexions dans le pool"
    )
    EXCEL_DATABASE_URL: str = Field(
        default="database.xlsx", description="URL de la base de données excel."
    )

    # authentification (JWT)
    JWT_SECRET_KEY: str = Field(default="mydevsecretkey", description="Clé secrète JWT")
    JWT_ALGORITHM: str = Field(
        default="HS256", description="Algorithme de signature JWT"
    )
    JWT_ACCESS_TOKEN_EXPIRES: timedelta | None = Field(
        default=None,
        description="Durée d'expiration du token d'accès (None = permanent)",
    )

    # .env mapper
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
