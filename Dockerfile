FROM python:3-alpine@sha256:323a717dc4a010fee21e3f1aac738ee10bb485de4e7593ce242b36ee48d6b352

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
