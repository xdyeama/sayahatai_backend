from app import database

from repository.repository import DestinationRepository
from .adapters.s3_service import S3Service
from app.trips.service import here_api_key
from .adapters.here_service import HereService


class Service:
    def __init__(self, repository: DestinationRepository, s3_service: S3Service,
                  here_service: HereService):
        self.repository = repository
        self.s3_service = s3_service
        self.here_service = here_service


def get_service():
    repository = DestinationRepository(database)
    s3_service = S3Service()
    here_service = HereService(here_api_key)
    svc = Service(repository, s3_service, here_service)

    return svc

