from apscheduler.schedulers.background import BackgroundScheduler
import os
import json


def send_channel(advertisement_str):
    os.system('python send_channel.py')


def init():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_channel, 'interval', seconds=10)
    scheduler.start()
