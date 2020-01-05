FROM python:alpine3.7


COPY requirements.txt /

RUN pip3 install -r /requirements.txt

WORKDIR /app

COPY ping_bot.py /app/

EXPOSE 80

CMD [ "python", "ping_bot.py" ]
