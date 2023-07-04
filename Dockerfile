FROM python:3.10.6

WORKDIR /test_task

COPY requirements.txt .

COPY main ./main

RUN python -m pip install -r requirements.txt

EXPOSE 8080


