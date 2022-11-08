FROM python:3.8-slim

WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
# create logs directory
RUN mkdir -p logs

ARG PORT
ARG WORKERS
ARG THREADS=1
ENV PORT=$PORT WORKERS=$WORKERS THREADS=$THREADS
EXPOSE $PORT

CMD gunicorn -b 0.0.0.0:$PORT --workers=$WORKERS auth.wsgi
