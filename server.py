#Generates a flask webapp that can have requests sent to it to keep
#the webserver up. Use cron-job.org to send periodic requests.

from flask import Flask
from threading import Thread
from datetime import datetime
import pytz

app = Flask('EVE')


@app.route('/')
def home():
  now = datetime.now(pytz.timezone('US/Eastern'))
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  return '<meta http-equiv="refresh" content="60" /> The current time is {}.'.format(
    dt_string)


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
