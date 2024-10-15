FROM python:3.10-slim-buster

WORKDIR /django_blog

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]