# VIA - Very Important App

This repository is a basic scaffold for a containerized app. It makes use of environment variables for configuration and is meant as part of a Kubernetes kickstart.

## Knobs & Wheels

The following environment variables are used:
- `VERSION` - shown as-is 
- `STAGE` - if either `dev`, `int` or `prod`, loads a corresponding stylesheet 
- `PORT` - used by gunicorn, which binds to this port

Furthermore, the whole env is visible in the app.

## Dependencies

```bash
cd app
python -m venv .venv  # do this in a virtual environment to isolate dependencies
source .venv/bin/activate  # actually use the new environment in this shell
pip install -r requirements.txt  # install dependencies
``` 

## Usage

You can run this either with flask directly:
```bash
cd app
flask --app app run
```

or using gunicorn as aWSGI server:
```bash
cd app
./serve.sh
``` 

## Building

```bash
TAG=chtime/via:latest
podman build -t $TAG .
```

## Deploying on OpenShift

You can directly import this via the OpenShift console into a cluster. More details are in [resources](./resources/README.md).
