FROM python:3.6.5
LABEL maintainer hopax-film-index
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api
COPY . /docker_api
RUN pip install pip==9.0.1
RUN pip install -r requirements.txt