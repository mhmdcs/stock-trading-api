from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_connection_string: str
    rapidapi_host: str
    rapidapi_key: str
    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_queue: str

    class Config:
        env_file = ".env"

settings = Settings()
