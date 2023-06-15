from app.config import database
from pydantic import BaseSettings

from .adapters.jwt_service import JwtService
from .adapters.s3_service import S3Service
from .adapters.here_service import HereService
from .repository.repository import ShanyraksRepository

from ..auth.service import config


class Settings(BaseSettings):
    HERE_API_KEY: str

    class Config:
        env_file = ".env"


here_api_key = Settings().dict()["HERE_API_KEY"]


class Service:
    def __init__(
        self,
        repository: ShanyraksRepository,
        jwt_svc: JwtService,
        here_svc: HereService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.s3_service = S3Service()
        self.here_service = here_svc


def get_service():
    repository = ShanyraksRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    here_svc = HereService(here_api_key)
    svc = Service(repository, jwt_svc, here_svc)
    return svc
