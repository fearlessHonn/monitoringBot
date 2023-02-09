from config import REFRESH_INTERVAL
from time import sleep


seconds = 1674514800
print(seconds % (REFRESH_INTERVAL * 3600))
print(f'New day: {seconds % (REFRESH_INTERVAL * 60 * 60) == 0}')
