"""NiceGUI frontend application — modular page structure.

All pages are defined in nicegui_app/pages/ and registered via @ui.page decorators.
This module creates the FastAPI sub-application and binds NiceGUI to it.
"""

from fastapi import FastAPI
from nicegui import ui

# Import all page modules to trigger @ui.page registrations
import nicegui_app.pages  # noqa: F401

# Import template modules to trigger layout registrations
import nicegui_app.templates.standard_intro   # noqa: F401
import nicegui_app.templates.standard_toc     # noqa: F401
import nicegui_app.templates.standard_contact  # noqa: F401
import nicegui_app.templates.standard_chart_left  # noqa: F401


def create_nicegui_app() -> FastAPI:
    """Create the NiceGUI ASGI app to be mounted under /ui."""
    app = FastAPI()
    ui.run_with(app, mount_path="/ui")
    return app
