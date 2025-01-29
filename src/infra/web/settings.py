from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # general
    APP_NAME: str = Field(default="IAsimov api", description="app name")
    APP_VERSION: str = Field(default="0.0.1", description="app version")

    # server
    HOST: str = Field(default="127.0.0.1", description="server address")
    PORT: int = Field(default=5000, description="server port")
    SERVER_URL: str = Field(default="http://127.0.0.1:5000")

    # database
    DATABASE_URL: str = Field(default="sqlite:///./test.db", description="database url")
    DATABASE_ECHO: bool = Field(default=True, description="enable SQL logs")
    DATABASE_POOL_SIZE: int = Field(
        default=5, description="max number of connections in pool"
    )

    # .env mapper
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
