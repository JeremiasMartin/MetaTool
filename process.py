import os
import subprocess
import json

exiftool_exe = r'.\exiftool.exe'
root_path = r'.\PARA_TESTEO_SCRIPT_RTK'
ejemplo = r'.\ejemplo.json'


# Generating csv file exiftool results (filename - rtkflag - CameraModel)
jsonfile = open(ejemplo, "w")
exiftool_command = [exiftool_exe, root_path, '-filename',
                    '-rtkflag', '-Model', '-q', '-j', '-r', '-W+', ejemplo]  # https://www.exiftool.org/exiftool_pod.html#OPTIONS
process = subprocess.run(exiftool_command)
jsonfile.close()