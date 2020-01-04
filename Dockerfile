FROM python:alpine3.7

ARG MC_LOGIN
ENV MC_LOGIN $MC_LOGIN
ARG MC_PASS 
ENV MC_PASS $MC_PASS
ARG TEST_URL  
ENV TEST_URL $TEST_URL
ARG SLACK_WEBHOOK
ENV SLACK_WEBHOOK $SLACK_WEBHOOK


COPY requirements.txt /

WORKDIR /app

RUN printenv

RUN pip3 install -r /requirements.txt && printf "USER_NAME=$MC_LOGIN\nUSER_PASSWORD=$MC_PASS\nTEST_URL='$TEST_URL'\nSLACK_HOOK_URL='$SLACK_WEBHOOK'" > /app/.env

COPY ping_bot.py /app/

EXPOSE 80

CMD [ "python", "./ping_bot.py" ]
