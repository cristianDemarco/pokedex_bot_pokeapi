FROM python:3.13.0a2-bookworm

WORKDIR /app

COPY requirements.txt  .

RUN pip install -r requirements.txt

COPY src src

COPY TOKEN.py .

CMD [ "python3", "src/bot.py" ]




