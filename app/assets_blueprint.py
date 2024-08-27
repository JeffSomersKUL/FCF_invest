import json
from pathlib import Path

from flask import current_app
from flask import Blueprint


class IncorrectNpmBuildError(Exception):
    pass


class IncorrectNpmConfigurationError(Exception):
    pass


SRC_DIR = Path(__file__).parent

frontend_blueprint = Blueprint(
    "assets_blueprint",
    __name__,
    static_folder=f"{SRC_DIR}/frontend/assets_compiled/bundled",
    static_url_path="/assets/bundled",
)


def _is_dev_environment():
    return current_app.config["ENVIRONMENT"] == "development"


def _get_assets(file_path):
    cfg = current_app.config
    if _is_dev_environment():
        current_app.logger.debug("App running in development environment")
        return f"{cfg['VITE_ORIGIN']}/assets/{file_path}"

    manifest_path = SRC_DIR / "frontend" / "assets_compiled" / "manifest.json"
    if not manifest_path.is_file():
        raise IncorrectNpmBuildError("Manifest file could not be found")

    try:
        with open(manifest_path, "r") as content:
            manifest = json.load(content)
        return f"/assets/{manifest[file_path]['file']}"
    except Exception as e:
        raise IncorrectNpmConfigurationError(
            f"Could not find file {file_path} in manifest"
        ) from e


@frontend_blueprint.app_context_processor
def add_context():
    return {
        "asset": _get_assets,
        "is_development": _is_dev_environment(),
    }
