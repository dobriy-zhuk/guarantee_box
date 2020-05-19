FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /my
WORKDIR /my
COPY requirements.txt /my/
RUN pip install -r requirements.txt
COPY . /my/
