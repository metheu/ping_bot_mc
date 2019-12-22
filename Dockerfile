FROM python:alpine3.7

COPY requirements.txt /

WORKDIR /app

RUN pip3 install -r /requirements.txt && printf "USER_NAME=$MC_LOGIN\nUSER_PASSWORD=$MC_PASS\nTEST_URL='$TEST_URL'\nSLACK_HOOK_URL='$SLACK_WEBHOOK'" > .env

COPY ping_bot.py .env /app/

EXPOSE 80

CMD [ "python", "./ping_bot.py" ]
