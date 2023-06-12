import os.path
import datetime
from pathlib import Path

def data_directory():
    """Creates directory for data if it doesn't exist
    and returns path to this directory"""
    dt = os.path.join(os.environ['USERPROFILE'], 
                      "OneDrive - University of Waterloo",
                      'Desktop')
    date = datetime.datetime.now().strftime("%Y%m%d")

    data_directory = os.path.join(dt, date)
    Path(data_directory).mkdir(exist_ok=True)
    return data_directory
