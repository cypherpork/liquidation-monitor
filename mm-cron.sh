#!/bin/bash -l
export PATH=$PATH:/usr/local/sbin:/usr/local/bin
env >> /home/parallels/makermonitor/crontab.log 2>&1
python /home/parallels/makermonitor/checker.py >> /home/parallels/makermonitor/crontab.log 2>&1
exit 0

