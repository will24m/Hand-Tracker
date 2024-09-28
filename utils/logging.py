import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='logs/hand_gestures.log', level=logging.INFO)

def log_event(event):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"{timestamp}: {event}")
