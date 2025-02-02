import logging
import os
from datetime import datetime

##Logging config
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path=os.path.join(os.getcwd(),"logs")  ### Creating a logs file in current worling directory(cwd)
os.makedirs(log_path, exist_ok=True)  ### if the log file already exists, it will not create a new one

log_file_path=os.path.join(log_path, LOG_FILE) ##total path

logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
