from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
