FROM python:3.9

WORKDIR /DE_task

COPY ./requirements.txt /DE_task/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /DE_task/requirements.txt

COPY ./app /DE_task/app

COPY ./02-src-data /DE_task/02-src-data/

CMD ["uvicorn", "app.server:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]