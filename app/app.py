import logging
import os

from flask import Flask, render_template, url_for

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)


@app.route("/")
def root():
    return render_template("root.html", **_template_args())


@app.route("/env")
def env():
    return render_template("env.html", **_template_args(env=dict(os.environ)))


@app.route("/volumes")
def volumes():
    cfg_volumes_path = os.environ.get("VOLUMES_PATH")
    if not cfg_volumes_path:
        logger.warning("VOLUMES_PATH environment variable not set")
        return render_template("volumes.html", **_template_args(unavailable=True))

    # Ensure the path exists
    if not os.path.exists(cfg_volumes_path):
        logger.error(f"Configured volume path does not exist: {cfg_volumes_path}")
        return render_template("volumes.html", **_template_args(unavailable=True))

    file_links = []
    for root, dirs, files in os.walk(cfg_volumes_path):
        for file in files:
            # Get the relative path from cfg_volumes_path
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, cfg_volumes_path)

            # Create URL using the relative path
            path = url_for("volume_file", subpath=relative_path)
            file_links.append(path)
            logger.debug(f"Added file: {relative_path} -> {path}")

    return render_template("volumes.html", **_template_args(files=file_links))


@app.route("/volumes/<path:subpath>")
def volume_file(subpath):
    cfg_volumes_path = os.environ.get("VOLUMES_PATH")
    if not cfg_volumes_path:
        logger.warning("VOLUMES_PATH environment variable not set")
        return "Volume path not configured", 500

    # Safely join paths and prevent directory traversal
    try:
        file_path = os.path.normpath(os.path.join(cfg_volumes_path, subpath))
        # Ensure the file_path is still within cfg_volumes_path
        if not file_path.startswith(os.path.normpath(cfg_volumes_path)):
            logger.warning(f"Attempted directory traversal: {subpath}")
            return "Invalid file path", 403
    except Exception as e:
        logger.error(f"Error constructing file path: {e}")
        return "Invalid file path", 400

    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return f"File {subpath} not found", 404

    if not os.path.isfile(file_path):
        logger.warning(f"Path is not a file: {file_path}")
        return f"Path {subpath} is not a file", 400

    try:
        file_name = os.path.basename(file_path)
        with open(file_path) as f:
            file_contents = f.readlines()
        logger.debug(
            f"Successfully read file: {file_path} ({len(file_contents)} lines)"
        )
        return render_template(
            "volumes.html",
            **_template_args(file_name=file_name, file_content=file_contents),
        )
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return "Error reading file", 500


@app.route("/image/static/")
@app.route("/image/static/<variant>")
def static_image(variant="a"):
    image_options = {
        "a": "66-800x400.jpg",
        "b": "894-800x400.jpg",
        "c": "237-800x400.jpg",
    }
    image_path = image_options.get(variant, "237-800x400.jpg")
    return render_template("image.html", **_template_args(image_file_name=image_path))


def _get_version() -> str:
    proxy_key = os.environ.get("VERSION_PROXY")
    if proxy_key:
        return os.environ.get(proxy_key, "n/a")
    else:
        return os.environ.get("VERSION", "n/a")


def _template_args(**extra_args) -> dict:
    default_args = {
        "version": _get_version(),
        "stage": os.environ.get("STAGE", "dev"),
        "message": os.environ.get("MESSAGE"),
    }
    return {**default_args, **extra_args}
