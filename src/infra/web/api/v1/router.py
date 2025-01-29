from flask_openapi3 import APIBlueprint  # type: ignore[attr-defined]

from infra.web.api.v1.routes.book_routes import router as book_router

routers = APIBlueprint(
    "/",
    __name__,
    url_prefix="/v1",
)


router_list = [book_router]

for router in router_list:
    routers.register_api(router)
