from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    BASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    # Email
    MAILJET_SMTP_SERVER:str
    MAILJET_SMTP_PORT: int
    MAILJET_USERNAME:str
    MAILJET_PASSWORD: str
    MAIL_FROM:str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()