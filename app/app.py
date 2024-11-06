import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("root.html", **_template_args())


@app.route('/env')
def env():
    return render_template("env.html", **_template_args(env=dict(os.environ)))


def _template_args(**extra_args) -> dict:
    default_args = {
        "version": os.environ.get("VERSION", "n/a"),
        "stage": os.environ.get("STAGE", "dev")
    }
    return {
        **default_args,
        **extra_args
    }
