FROM python:3.9-slim
# Set timezone
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# get files
RUN apt-get update
RUN apt install cron -y
RUN apt-get install -q -y rsyslog

# Debug tool
RUN apt install nano

# Export TZ ENV
RUN TZ=Europe/Berlin
RUN export TZ

# Project
COPY /data/ /scraper/data/
COPY main.py /scraper/
RUN chmod +x /scraper/
COPY crontab /etc/cron.d/
RUN chmod +x /etc/cron.d/crontab

RUN crontab /etc/cron.d/crontab

WORKDIR /scraper/

CMD /usr/sbin/cron -f
# docker build -t frb_park .
# docker save -o ./frb_park.tar frb_park
# docker run -it -v data:/scraper/data frb_park:latest
