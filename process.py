import os
import subprocess
import pandas as pd


exiftool_exe = r'E:\exiftool.exe'
root_path = r'E:\PARA_TESTEO_SCRIPT_RTK'
ejemplo = r'E:\ejemplo.csv'


RTKFLAG0, RTKFLAG16, RTKFLAG34, RTKFLAG50 = 0, 0, 0, 0

# Generating csv file exiftool results (filename - rtkflag - CameraModel)
csv = open(ejemplo, "w")
for path, dirs, files in os.walk(root_path):
    for file in files:
        file_path = path + os.sep + file
        ext = file.split(".")[1]
        if(ext == 'JPG' or ext == 'jpg' or ext == 'JPEG' or ext == 'jpeg'):
            exiftool_command = [exiftool_exe, file_path, '-filename',
                                '-rtkflag', '-Model', '-q', '-T', '-W+', ejemplo]
            process = subprocess.run(exiftool_command)
csv.close()


# Generating txt file, calculating data from csv

df = pd.read_csv(ejemplo, header=None, sep='\t', usecols=[1])

for i in df.values:
    if(i == '16'):
        RTKFLAG16 = RTKFLAG16 + 1
    elif(i == '50'):
        RTKFLAG50 = RTKFLAG50 + 1
    elif(i == '0'):
        RTKFLAG0 = RTKFLAG0 + 1
    elif(i == '34'):
        RTKFLAG34 = RTKFLAG34 + 1

TOTAL = df.size
OTHERS = TOTAL - RTKFLAG0 - RTKFLAG16 - RTKFLAG34 - RTKFLAG50

txt = open(r'E:\final.json', "w")
txt.write('{\n "P4RTK":{\n "0": ' + str(RTKFLAG0) + ',\n "16": ' + str(RTKFLAG16) + ',\n 34: ' + str(RTKFLAG34) + ',\n 50: ' +
          str(RTKFLAG50) + '\n }, \n other: ' + str(OTHERS) + ', total: ' + str(TOTAL) + '}')
txt.close()


# FC350 = INSPIRE1
# FC300X = P3
# FC6310 = P4P
# FC610S = P4PV2
# FC6310R = P4PRTK
# L1D-20C = MAVIC2P
