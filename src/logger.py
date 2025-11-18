import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs")
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH, 
    level=logging.INFO, 
    format='[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__)

#test logging
logging.info("Logging is set up.")

# if __name__ == "__main__":
#     try:
#         logging.info("This is a test log message.")
#         a = 1 / 0
#     except Exception as e:
#         logging.info("Exception occurred")
#         raise exception.CustomException(e, sys)