FROM python:3.10-slim

WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# run `docker build -t investor-bulletin -f dev_setup/Dockerfile .`
# then `docker run -p 8000:8000 investor-bulletin` to test.
