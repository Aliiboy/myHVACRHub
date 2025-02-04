from flask_openapi3 import APIBlueprint  # type: ignore[attr-defined]

from infra.web.api.v1.routes.book_routes import router as book_router
from infra.web.api.v1.routes.humid_air_routes import router as humid_air_router
from infra.web.api.v1.routes.user_routes import router as user_router

security = [{"jwt": []}]  # type: ignore[var-annotated]

routers = APIBlueprint(
    "/",
    __name__,
    url_prefix="/v1",
    abp_security=security,
)


router_list = [book_router, humid_air_router, user_router]

for router in router_list:
    routers.register_api(router)
