FROM python:3.12.3-alpine
ARG ENV_FILE
RUN apk upgrade
RUN apk add gcc build-base python3-dev musl-dev \
			libc-dev libcurl curl-dev gpgme-dev make libmagic jpeg-dev \
			zlib-dev libjpeg supervisor bash ffmpeg git \
                        libxml2-dev libxslt-dev dcron
RUN mkdir -p /usr/src/environments/easyimovel && mkdir /mnt/scrappers
WORKDIR /usr/src/environments/easyimovel/
# RUN git clone -b master https://github.com/muhbianco/APIUtils.git .
COPY ./. .
COPY $ENV_FILE .env
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
RUN chmod +x /usr/src/environments/easyimovel/entrypoint.sh
RUN chmod +x /usr/src/environments/easyimovel/services/chromedriver
COPY crontab /etc/cron.d/olx-cron
RUN chmod 0644 /etc/cron.d/olx-cron
RUN crontab /etc/cron.d/olx-cron
RUN touch /var/log/cron.log
ENTRYPOINT ["/usr/src/environments/easyimovel/entrypoint.sh"]
