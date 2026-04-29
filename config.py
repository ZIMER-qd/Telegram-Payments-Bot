from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    provider_token: SecretStr
    postgre_pass: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

config = Settings()