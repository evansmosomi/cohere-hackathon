FROM python:3.11

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

EXPOSE python3.11 ravenpack.py
