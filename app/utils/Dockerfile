FROM python:3.9.11-slim

COPY requirements.txt ./
RUN apt update
RUN apt install -y libmariadb-dev cron nano dos2unix gfortran libopenblas-dev liblapack-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY /system/app/ /app/
COPY /system/jobs/crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

RUN dos2unix /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

WORKDIR /app

RUN python3 get_btc_data.py
RUN python3 meme_index.py


CMD ["cron", "-f"]