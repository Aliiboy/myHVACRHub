import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from common.infra.web.app import WebApp  # noqa: I001
from common.infra.web.container import AppContainer

# container
container = AppContainer()
container.init_resources()

# app
app = WebApp(container=container).app

if __name__ == "__main__":
    app.run()
