
#
# basic defs
WIDTH = 600
HEIGHT = 400
FPS = 60
TITLE = "Parking"
FONT_NAME = "arial"

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# layers
# cars should go under (be shadowed by) sensors
CAR_LAYER = 1
CAR_SENSOR_LAYER = 2
STAIRS_LAYER = 2
LIGTHS_LAYER = 1

WAITING, PARKING, PARKED, LEAVING = range(4)

#
RANDOM_MOVES_INTERVAL = 0.5
RANDOM_PARK_TRY_ANY_CAR = True

#
import time
DATETIME_FMT = "%Y/%m/%d %H:%M:%S"
def format_datetime(format=DATETIME_FMT, when=None):
    if when is None:
        return time.strftime(DATETIME_FMT)
    else:
        return time.strftime(DATETIME_FMT, when)

def format_sec(format=DATETIME_FMT, sec=None):
    if sec is None:
        sec = now()
    return format_datetime(format=format, when=time.localtime(sec))

def str_now():
    return time.strftime(DATETIME_FMT)

def sec_to_datetime(sec):
    pass

def now():
    return int(time.time())
