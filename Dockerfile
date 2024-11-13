FROM python:3-alpine@sha256:c38ead8bcf521573dad837d7ecfdebbc87792202e89953ba8b2b83a9c5a520b6

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
