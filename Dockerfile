FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /guarantee
WORKDIR /guarantee
COPY requirements.txt /guarantee/
RUN pip install -r requirements.txt
COPY . /guarantee/
