# VIA - Very Important App

This repository is a basic scaffold for a containerized app. It makes use of environment variables for configuration and is meant as part of a Kubernetes kickstart.

## Knobs & Wheels

The following environment variables are used:
- `VERSION` - shown as-is 
- `STAGE` - if either `dev`, `int` or `prod`, loads a corresponding stylesheet 
- `PORT` - used by gunicorn, which binds to this port

Furthermore, the whole env is visible in the app.

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
