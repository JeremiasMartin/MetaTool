import subprocess
import json

exiftool_exe = r'E:\exiftool.exe'
root_path = r'E:\PARA_TESTEO_SCRIPT_RTK'
data = r'E:\data.json'


# Generating json file using exiftool (filename - rtkflag - cameraModel)
exiftool_command = [exiftool_exe, root_path, '-filename',
                    '-rtkflag', '-Model', '-q', '-json', '-r']  # https://www.exiftool.org/exiftool_pod.html#OPTIONS

with open(data, "w") as f:
    process = subprocess.run(exiftool_command, stdout=f)


rtkflags = {}
cameramodels = {}