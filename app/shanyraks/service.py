
from app.config import database

from .adapters.jwt_service import JwtService
from .repository.repository import ShanyraksRepository

from ..auth.service import config


class Service:
    def __init__(
        self,
        repository: ShanyraksRepository,
        jwt_svc: JwtService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc


def get_service():
    repository = ShanyraksRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)

    svc = Service(repository, jwt_svc)
    return svc
