from dependency_injector.wiring import Provide, inject
from flask_openapi3 import OpenAPI, Server  # type: ignore[attr-defined]
from flask_openapi3.models.info import Info

from infra.web.api.v1.router import routers as routers_v1
from infra.web.container import AppContainer
from utils.class_object import singleton


@singleton
class WebApp:
    @inject
    def __init__(self, container: AppContainer = Provide[AppContainer]) -> None:
        # container
        self.container = container
        self.settings = self.container.app_settings()

        # app
        servers = [Server(url=self.settings.SERVER_URL)]
        info = Info(title=self.settings.APP_NAME, version=self.settings.APP_VERSION)
        self.app = OpenAPI(__name__, info=info, servers=servers)

        # database
        self.database = self.container.database()
        self.database.create_database()

        # routes
        self.app.register_api(routers_v1)

    def run(self) -> None:
        self.app.run(host=self.settings.HOST, port=self.settings.PORT)
