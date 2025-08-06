FROM python:3.10

WORKDIR /app

COPY ./messaging_app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./messaging_app .

RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN pip install mysqlclient

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

RUN useradd messaging_app_user
USER messaging_app_user

CMD ["python", "manage.py", "runserver", "0.0.0.0", "-p", "8000"]