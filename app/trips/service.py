from app.config import database
from pydantic import BaseSettings

from .repository.repository import TripsRepository
from .adapters.s3_service import S3Service
from .adapters.here_service import HereService
from .adapters.openai_service import LLMService


class Settings(BaseSettings):
    HERE_API_KEY: str

    class Config:
        env_file = ".env"


here_api_key = Settings().dict()["HERE_API_KEY"]


class Service:
    def __init__(
        self,
        repository: TripsRepository,
        s3_service: S3Service,
        here_service: HereService,
        openai_service: LLMService,
    ):
        self.repository = repository
        self.s3_service = s3_service
        self.here_service = here_service
        self.openai_service = openai_service


def get_service():
    repository = TripsRepository(database)
    s3_svc = S3Service()
    here_service = HereService(here_api_key)
    openai_service = LLMService()
    svc = Service(repository, s3_svc, here_service, openai_service)
    return svc
