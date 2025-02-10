from flask_openapi3 import APIBlueprint  # type: ignore[attr-defined]

from infra.web.api.v1.routes.book_routes import router as book_router
from infra.web.api.v1.routes.fast_quote_routes import router as fast_quote_router
from infra.web.api.v1.routes.humid_air_routes import router as humid_air_router
from infra.web.api.v1.routes.protected_routes import router as protected_router
from infra.web.api.v1.routes.user_routes import router as user_router

routers = APIBlueprint(
    "/",
    __name__,
    url_prefix="/v1",
)


router_list = [
    book_router,
    humid_air_router,
    user_router,
    protected_router,
    fast_quote_router,
]

for router in router_list:
    routers.register_api(router)
