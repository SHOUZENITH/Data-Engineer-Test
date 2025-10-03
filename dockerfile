FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./solution ./solution
COPY ./data ./data

CMD ["python", "solution/Solution.py"]