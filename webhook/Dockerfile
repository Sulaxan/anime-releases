FROM alpine

# make anime-releases be a directory at the root
RUN mkdir /anime-releases/
ADD webhook/ /anime-releases/webhook/
ADD requirements.txt .

RUN mkdir jobs/
ADD ar-crobjob jobs/ar-cronjob

# Install Python/Pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip

RUN pip3 install --no-cache --upgrade pip
RUN pip3 install -r requirements.txt

# setup cron job
RUN crontab jobs/ar-cronjob

CMD ["crond", "-f"]
