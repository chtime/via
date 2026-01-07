FROM python:3-alpine@sha256:e7e041128ffc3e3600509f508e44d34ab08ff432bdb62ec508d01dfc5ca459f7

LABEL org.opencontainers.image.source="https://github.com/chtime/via"

ARG BUILD_VERSION
ARG BUILD_DATE
ENV VERSION=${BUILD_VERSION}
ENV BUILD_DATE=${BUILD_DATE}

EXPOSE 8000

WORKDIR /app
ADD app /app
RUN pip install -r requirements.txt

CMD "./serve.sh"
