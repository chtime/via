FROM python:3-alpine@sha256:c38ead8bcf521573dad837d7ecfdebbc87792202e89953ba8b2b83a9c5a520b6

LABEL org.opencontainers.image.source="https://github.com/chtime/via"

EXPOSE 8000

WORKDIR /app
ADD app /app
RUN pip install -r requirements.txt

CMD "./serve.sh"
