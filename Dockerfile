FROM python:3.11

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

RUN python ravenpack.py

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
