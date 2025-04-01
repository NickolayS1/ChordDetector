import logging
from logging.handlers import TimedRotatingFileHandler
import os

os.makedirs("./logs", exist_ok=True)

handler = TimedRotatingFileHandler(
    "./logs/app.log",
    when="D",       # Daily rotation
    interval=1,     # Every 1 day
    backupCount=2   # Keep 2 days of logs
)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler]
)