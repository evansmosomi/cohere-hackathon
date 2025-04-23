FROM python:3.11

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python3.11 ravenpack.py

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
