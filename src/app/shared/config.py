from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./src/.env")

    username: str = Field(..., alias="DATABASE_USER")
    password: str = Field(..., alias="DATABASE_PASSWORD")
    database: str = Field(..., alias="DATABASE_NAME")
    host: str = Field(..., alias="DATABASE_HOST")
    port: int = Field(..., alias="DATABASE_PORT")

    development: bool = Field(False, alias="DEVELOPMENT")

    @computed_field
    @property
    def get_connection_string(self) -> str:
        return f"mongodb+srv://{self.username}:{self.password}@{self.host}/?retryWrites=true&w=majority&appName={self.database}"
