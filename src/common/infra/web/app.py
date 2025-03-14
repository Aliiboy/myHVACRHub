from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response, jsonify
from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Server  # type: ignore[attr-defined]
from flask_openapi3.models.info import Info
from werkzeug.exceptions import HTTPException

from common.infra.web.api.v1.router import routers as routers_v1
from common.infra.web.container import AppContainer
from utils.class_object import singleton


@singleton
class WebApp:
    """Application web

    Args:
        container (AppContainer): Conteneur de l'application
    """

    @inject
    def __init__(self, container: AppContainer = Provide[AppContainer]) -> None:
        """Initialise l'application web

        Args:
            container (AppContainer, optional): Conteneur de l'application
        """
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

        # error handlers
        @self.app.errorhandler(Exception)
        def handle_exception(e: Exception) -> tuple[Response, int]:
            """Handle all exceptions."""
            if isinstance(e, HTTPException):
                response = jsonify(message=str(e))
                response.status_code = (
                    e.code if e.code else HTTPStatus.INTERNAL_SERVER_ERROR
                )
            else:
                response = jsonify(message=str(e))
                response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response, response.status_code

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

    def run(self: "WebApp") -> None:
        """Démarre l'application web

        Args:
            self (WebApp): Instance de l'application web
        """
        self.app.run(host=self.settings.HOST, port=self.settings.PORT)
