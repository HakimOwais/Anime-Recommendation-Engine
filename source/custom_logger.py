import logging
import os
from datetime import datetime

# Create a log directory variable where we save logs
LOG_DIR = 'logs'

# Create a directory under the name logs
LOGS = os.makedirs(LOG_DIR, exist_ok=True)

# We now create a log file which stores logs in logs directory
LOG_FILE = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logger = logging.basicConfig(
    filename=LOG_FILE,  # Set the filename for log output.
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format.
    level=logging.INFO  # Set the logging level to INFO.
)

# Create custom logging inheriting python logging as well
def get_logger(name):
    # Create a logger with the given name
    logger = logging.getLogger(name)
    # Setting the logger level to INFO
    logger.setLevel(logging.INFO)
    return logger


