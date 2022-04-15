FROM python:3.7

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/assistant_api

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8002"]
