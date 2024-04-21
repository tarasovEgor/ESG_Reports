FROM python:3.12-slim

RUN apt-get update

RUN apt-get install -y poppler-utils

COPY . /

WORKDIR /

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN chmod 777 pdf2text

EXPOSE 5000


CMD ["python", "main.py"]
