FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
#ADD requirements.txt /code/


COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code