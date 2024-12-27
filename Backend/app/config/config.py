import os

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    ML_SERVER_HOST: str
    ML_SERVER_PORT: str
    ML_PREDICT_ROUTER: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            ".env"
        )
    )


settings = Settings()


def get_db_url() -> str:
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_jwt_settings() -> dict[str, str]:
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
    }


def get_ml_server_query_url() -> str:
    return f"http://172.22.0.2:8002/ml/predict/"
