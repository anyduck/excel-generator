FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app
COPY ./public /app/public

RUN pip install --upgrade pip
RUN ls -agl
RUN pip install -r ./app/requirements.txt