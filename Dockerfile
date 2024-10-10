FROM python:3.12-slim-bookworm

WORKDIR /usr/src/macdii
COPY . .

RUN pip install .

ENTRYPOINT [ "python", "-m", "macdii" ]