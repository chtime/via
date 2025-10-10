FROM python:3-alpine@sha256:829edcc737417f9084a154511bde03a50b7996f3746e4c8a6b30a99a9a10648c

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
