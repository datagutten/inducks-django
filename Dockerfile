###########
# BUILDER #
###########

# pull official base image
FROM python:3.12-bookworm AS builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip poetry poetry-plugin-export

COPY pyproject.toml .

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with mysql --with postgres
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels gunicorn

#########
# FINAL #
#########

FROM python:3.12-slim-bookworm

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends default-libmysqlclient-dev
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
RUN pip install psycopg2-binary


# copy project
COPY . $APP_HOME
WORKDIR $APP_HOME

# chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# change to the app user
# USER app
# RUN python manage.py makemigrations

RUN chmod +x launcher.sh
CMD /home/app/web/launcher.sh