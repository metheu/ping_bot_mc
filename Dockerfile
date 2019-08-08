FROM python:alpine3.7

COPY requirements.txt /

WORKDIR /app

RUN pip3 install -r /requirements.txt

COPY ping_bot.py .env /app/

EXPOSE 80

CMD [ "python", "./ping_bot.py" ]
