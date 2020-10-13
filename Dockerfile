FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
COPY ./public /public
COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN ls -agl
RUN pip install -r requirements.txt