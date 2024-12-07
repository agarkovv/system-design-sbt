FROM python:3.9

COPY main.py main.py

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt requirements.txt

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install -r requirements.txt

EXPOSE 80