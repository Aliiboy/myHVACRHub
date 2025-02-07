from dependency_injector.wiring import Provide, inject
from flask_jwt_extended import JWTManager
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

        # security
        jwt = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        security_schemes = {"jwt": jwt}
        # app
        servers = [Server(url=self.settings.SERVER_URL)]
        info = Info(title=self.settings.APP_NAME, version=self.settings.APP_VERSION)
        self.app = OpenAPI(
            __name__,
            info=info,
            servers=servers,
            security_schemes=security_schemes,  # type: ignore[arg-type]
            doc_prefix="/",
        )

        # jwt
        self.app.config["JWT_SECRET_KEY"] = self.settings.JWT_SECRET_KEY
        self.app.config["JWT_ALGORITHM"] = self.settings.JWT_ALGORITHM
        self.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = (
            self.settings.JWT_ACCESS_TOKEN_EXPIRES
            if self.settings.JWT_ACCESS_TOKEN_EXPIRES is not None
            else False
        )
        self.jwt = JWTManager(self.app)

        # routes
        self.app.register_api(routers_v1)

    def run(self) -> None:
        self.app.run(host=self.settings.HOST, port=self.settings.PORT)
