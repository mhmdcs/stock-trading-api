FROM python:3.10-slim

WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
