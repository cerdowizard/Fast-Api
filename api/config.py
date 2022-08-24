from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    class Config:
        env_file = "api/.env"
        env_file_encoding = "utf-8"



























# import os
# from dotenv import load_dotenv
#
# from pathlib import Path
#
# env_path = Path('.') / '.env'
#
# load_dotenv(dotenv_path=env_path)
#
#
# class Settings:
#     DB_CONNECTION: str = os.getenv("DB_CONNECTION")
#     DB_HOST: str = os.getenv("DB_HOST")
#     DB_PORT: str = os.getenv("DB_PORT")
#     DB_DATABASE: str = os.getenv("DB_DATABASE")
#     DB_USERNAME: str = os.getenv("DB_USERNAME")
#     DB_PASSWORD: str = os.getenv("DB_PASSWORD")
#     DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
#
#
# settings = Settings()
