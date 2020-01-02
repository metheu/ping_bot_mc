FROM python:alpine3.7

ENV MC_LOGIN $MC_LOGIN
ENV MC_PASS $MC_PASS
ENV TEST_URL $TEST_URL
ENV SLACK_WEBHOOK $SLACK_WEBHOOK

COPY requirements.txt /

WORKDIR /app

RUN echo $MC_LOGIN && pip3 install -r /requirements.txt && printf "USER_NAME=$MC_LOGIN\nUSER_PASSWORD=$MC_PASS\nTEST_URL='$TEST_URL'\nSLACK_HOOK_URL='$SLACK_WEBHOOK'" > /app/.env

COPY ping_bot.py /app/

EXPOSE 80

CMD [ "python", "./ping_bot.py" ]
