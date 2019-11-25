import sys
import os

REAL_FILE_PATH = os.path.realpath(sys.argv[0])
SELF_PATH = str(os.path.abspath(os.path.join(REAL_FILE_PATH, os.pardir)))

HTML_PATH = os.path.join(SELF_PATH, "platforms", "res")
HTML_INDEX = os.path.join(HTML_PATH, "via.html")

HTML_PATH_TEMP = os.path.join(SELF_PATH, "platforms", "html")
TEMP_HTML = os.path.join(HTML_PATH_TEMP, "temp.html")

INI_PATH = os.path.join(SELF_PATH, "ini.yml")

IOU = 0.5
DISTANCE = 100
