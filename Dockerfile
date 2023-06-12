FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r /code/requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]