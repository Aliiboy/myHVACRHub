from flask_openapi3 import APIBlueprint  # type: ignore[attr-defined]

from humid_air.infra.web.api.v1.humid_air_routes import router as humid_air_router
from projects.infra.web.api.v1.project_routes import router as project_router
from users.infra.web.api.v1.user_routes import router as user_router

routers = APIBlueprint(
    "/",
    __name__,
    url_prefix="/v1",
)


router_list = [
    humid_air_router,
    user_router,
    project_router,
]

for router in router_list:
    routers.register_api(router)
