FROM python:3.9

ENV APPLICATION_SERVICE=/app

# set work directory
RUN mkdir -p $APPLICATION_SERVICE

# where the code lives
WORKDIR $APPLICATION_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# copy project
COPY . $APPLICATION_SERVICE

CMD python manage.py telegram_bot