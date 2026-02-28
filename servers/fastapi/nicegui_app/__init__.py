"""NiceGUI frontend application — modular page structure.

All pages are defined in nicegui_app/pages/ and registered via @ui.page decorators.
Register NiceGUI at /ui on the main FastAPI app via register_nicegui(app).
"""

from nicegui import ui

# Import all page modules to trigger @ui.page registrations
import nicegui_app.pages  # noqa: F401

# Import template modules to trigger layout registrations
import nicegui_app.templates.standard_intro   # noqa: F401
import nicegui_app.templates.standard_toc     # noqa: F401
import nicegui_app.templates.standard_contact  # noqa: F401
import nicegui_app.templates.standard_chart_left  # noqa: F401


def register_nicegui(app):
    """Register NiceGUI UI at /ui on the given FastAPI app. Call this after app creation."""
    ui.run_with(app, mount_path="/ui")
