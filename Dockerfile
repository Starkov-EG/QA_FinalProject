FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT pytest ./tests --alluredir allure-results
