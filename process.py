import os
import subprocess
import pandas as pd


exiftool_exe = r'C:\Users\Jeremias\Documents\exiftool.exe'
root_path = r'C:\Users\Jeremias\Documents\PARA_TESTEO_SCRIPT_RTK'
ejemplo = r'C:\Users\Jeremias\Documents\ejemplo.csv'


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

rtkflags = pd.read_csv(ejemplo, header=None, sep='\t', usecols=[1])
cameramodels = pd.read_csv(ejemplo, header=None, sep='\t', usecols=[2])


rtkflagsargs = {
    '0': 0,
    '16': 0,
    '34': 0,
    '50': 0
}

for i in rtkflags.values:
    if(i[0] != '-'):
        rtkflagsargs[i[0]] += 1


cameramodelsargs = {
    'FC350': 0,
    'FC300X': 0,
    'FC6310R': 0,
    'FC610S': 0,
    'L1D-20c': 0
}

for i in cameramodels.values:
    cameramodelsargs[i[0]] += 1


TOTAL = rtkflags.size

# writing output to a txt file
txt = open(r'C:\Users\Jeremias\Documents\final.json', "w")
txt.write('{\n')

for i in cameramodelsargs:
    value = cameramodelsargs.get(i)
    if(value > 0):
        # Check RTK flags if any image was taken with FC6310R model
        if(i == 'FC6310R'):
            txt.write('"FC6310R":{\n "0": ' + str(rtkflagsargs['0']) + ',\n "16": ' + str(
                rtkflagsargs['16']) + ',\n "34": ' + str(rtkflagsargs['34']) + ',\n "50": ' + str(rtkflagsargs['50']) + '\n },')
        txt.write('\n"' + i + '"' + ': ' + str(value) + ',')

txt.write('\n "_total": ' + str(TOTAL) + '\n }')
txt.close()
