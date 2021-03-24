import os
import pickledb # You can use any other database too. Use SQL if you are using Heroku Postgres.
import feedparser
from time import sleep, time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler

session_name = "AQA9tfNrZ3o9T7-C78ikEAOOTmn66V4K-Hcv6HNfmL7nuyntZMJVE3qjhGCz-piaIDZvGzuXpCSWpu-aCD0Vr5TvelIBuXwTJ-cfET7slwoieq1jOY3U7snVhB0PEal8hcFJbRTN82Hd5F-xs6A8-UgY9_pHckDPCprjiQX3pKGV9nkKZIwDI2aGvXI53Rrd287L2bVDicFnvFb8QEQbevciv7pAiHTUdNKG8P9Nme2bpLb76eI9cMGn2IEhD8KSxWEHmBEzhutVa71bnE5QhdEzfDJVyugSTfOR-Da_RNgtqVXzPxpPkTDOstjTP5YPqt7M2l8qre7rFaMcoqEIDiAiN3QeQgA"
api_id = "3751415"   # Get it from my.telegram.org
api_hash = "6547d1aaebb53eea6707945a48c4dd2f"   # Get it from my.telegram.org
feed_url = ["https://torrentgalaxy.to/rss?magnet"]   # RSS Feed URL of the site.
   # Get it by creating a bot on https://t.me/botfather
log_channel = "-1001478632499"   # Telegram Channel ID where the bot is added and have write permission. You can use group ID too.
check_interval = 5  # Check Interval in seconds.  
max_instances = 5   # Max parallel instance to be used.
if os.environ.get("ENV"):   # Add a ENV in Environment Variables if you wanna configure the bot via env vars.
  session_name= os.environ.get("SESSION_NAME")
  api_id = os.environ.get("APP_ID")
  api_hash = os.environ.get("API_HASH")
  feed_url = os.environ.get("FEED_URL")
  log_channel = int(os.environ.get("LOG_CHANNEL", None))
  check_interval = int(os.environ.get("INTERVAL", 30))
  max_instances = int(os.environ.get("MAX_INSTANCES", 5))

db = pickledb.load('rss.db', True)
if db.get("feed_url") == None:
  db.set("feed_url", "*")
app = Client(session_name=session_name, api_id=api_id, api_hash=api_hash)

def check_feed():
  for furl in feed_url:
    FEED = feedparser.parse(furl)
    entry = FEED.entries[0]
    if entry.id != db.get("feed_url"):
      message = f"{entry.link}"
      try:
        app.send_message(log_channel, message)
        db.set("feed_url", entry.id)
      except FloodWait as e:
        print(f"FloodWait: {e.x} seconds")
        sleep(e.x)
      except Exception as e:
        print(e)
    else:
      print(f"Checked RSS FEED: {entry.id}")



scheduler = BackgroundScheduler()
scheduler.add_job(check_feed, "interval", seconds=check_interval, max_instances=max_instances)
scheduler.start()
app.run()
