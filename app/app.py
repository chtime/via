import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("root.html", **_template_args())


@app.route('/env')
def env():
    return render_template("env.html", **_template_args(env=dict(os.environ)))


def _get_version() -> str:
    proxy_key = os.environ.get("VERSION_PROXY")
    if proxy_key:
        return os.environ.get(proxy_key, "n/a")
    else:
        return os.environ.get("VERSION", "n/a")

def _template_args(**extra_args) -> dict:
    default_args = {
        "version": _get_version(),
        "stage": os.environ.get("STAGE", "dev")
    }
    return {
        **default_args,
        **extra_args
    }
