FROM python:3.4
MAINTAINER Stefan Bokic <stefanbokic731@gmail.com>

RUN pip install --upgrade pip

RUN mkdir -p /usr/src/uksProject
WORKDIR /usr/src/uksProject

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./uksProject .

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
