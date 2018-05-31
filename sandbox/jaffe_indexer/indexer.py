import os

PATH = os.path.abspath(os.path.dirname(__file__)) + '\\'
HA_PATH = os.path.abspath(os.path.dirname(__file__)) + '\\HA\\'
NE_PATH = os.path.abspath(os.path.dirname(__file__)) + '\\NE\\'
SA_PATH = os.path.abspath(os.path.dirname(__file__)) + '\\SA\\'
SU_PATH = os.path.abspath(os.path.dirname(__file__)) + '\\SU\\'

for file in os.listdir():
    if file.endswith(".tiff"):
        if 'HA' in file:
            os.rename(PATH + file, HA_PATH + file)
        elif 'SU' in file:
            os.rename(PATH + file, SU_PATH + file)
        elif 'SA' in file:
            os.rename(PATH + file, SA_PATH + file)
        elif 'NE' in file:
            os.rename(PATH + file, NE_PATH + file)