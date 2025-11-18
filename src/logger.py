import logging
import os
import sys
from datetime import datetime
import exception

LOG_FILE=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH, 
    level=logging.INFO, 
    format='[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__)


# if __name__ == "__main__":
#     try:
#         logging.info("This is a test log message.")
#         a = 1 / 0
#     except Exception as e:
#         logging.info("Exception occurred")
#         raise exception.CustomException(e, sys)