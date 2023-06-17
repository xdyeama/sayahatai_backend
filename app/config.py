from typing import Any

from pydantic import BaseSettings
from pymongo import MongoClient
from dotenv import dotenv_values


class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    MONGOHOST: str = "localhost"
    MONGOPORT: str = "27017"
    MONGOUSER: str = "root"
    MONGOPASSWORD: str = "password"
    MONGODATABASE: str = "fastapi"
    HERE_API_KEY: str = dotenv_values("../.env").get("HERE_API_KEY")


# environmental variables
env = Config()

# FastAPI configurations
fastapi_config: dict[str, Any] = {
    "title": "Shanyrak.kz API",
}

# MongoDB connection
client = MongoClient(
    f"mongodb://{env.MONGOUSER}:{env.MONGOPASSWORD}@{env.MONGOHOST}:{env.MONGOPORT}/"
)

# MongoDB database
database = client[env.MONGODATABASE]
