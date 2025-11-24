import os
import sys
import pandas as pd
import numpy as np

import dill

from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass   

def save_object(file_path, obj):
    """Saves a Python object to a file using pickle."""
    try:
        
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)