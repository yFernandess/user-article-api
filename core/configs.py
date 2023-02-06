from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
    General settings used in the application
    """
    API_V1: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:12345678@localhost:5432/faculdade"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'BOatook12LMPN9QAHFaxCkwX5A6AyPAcrWrLEXanvtE'
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """

    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    """
    Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjc1ODc4OTkxLCJpYXQiOjE2NzUyNzQxOTEsInN1YiI6Mn0.pNLNamcYY2Y4xy6gRJrPjwleE23nWLc4oXOR8kZyc04
    Type: bearer
    """

    class Config:
        case_sensitive = True


settings: Settings = Settings()
