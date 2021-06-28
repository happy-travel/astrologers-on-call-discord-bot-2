FROM python:3.9.2-slim

ARG HTDC_ON_CALL_DISCORD_TOKEN

ENV HTDC_ON_CALL_DISCORD_TOKEN=$HTDC_ON_CALL_DISCORD_TOKEN

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir --ignore-installed

COPY . .

CMD ["python","-u","bot.py"]