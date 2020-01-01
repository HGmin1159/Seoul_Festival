#!/bin/bash

cd /home/ubuntu/web
git pull
cd /home/ubuntu/cron
git pull

/home/ubuntu/cron/final_auto_crawling_db_update.py >> /home/ubuntu/cron/log/cronlog.log 2>&1

/home/ubuntu/cron/man_proportion_prediction.R >> /home/ubuntu/cron/predlog.log

/home/ubuntu/cron/image_retriever.py >> /home/ubuntu/cron/log/cronlog.log 2>&1

/home/ubuntu/cron/sqltojson.py >> /home/ubuntu/cron/log/cronlog.log 2>&1

/home/ubuntu/cron/get_restaurant.py >> /home/ubuntu/cron/log/cronlog.log 2>&1

scp -i /home/ubuntu/.ssh/sfshiny.pem /home/ubuntu/cron/SEOUL_FESTIVAL.db ubuntu@ec2-35-170-234-69.compute-1.amazonaws.com:/home/ubuntu/sfplumber >> /home/ubuntu/cron/log/cronlog.log 2>&1

/home/ubuntu/cron/git-update.sh >> /home/ubuntu/cron/log/cronlog.log 2>&1

cd /home/ubuntu/web

/home/ubuntu/cron/git-update.sh >> /home/ubuntu/cron/log/cronlog.log 2>&1
