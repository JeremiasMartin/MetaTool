import subprocess
import json

exiftool_exe = r'C:\exiftool.exe'
root_path = r'C:\PARA_TESTEO_SCRIPT_RTK'
data = r'C:\data.json'


# Generating json file using exiftool (filename - rtkflag - cameraModel)
exiftool_command = [exiftool_exe, root_path, '-filename',
                    '-rtkflag', '-Model', '-q', '-json', '-fast', '-r', '-ext', 'JPG']  # https://www.exiftool.org/exiftool_pod.html#OPTIONS

with open(data, "w") as f:
    process = subprocess.run(exiftool_command, stdout=f)


rtkflags = {}
cameramodels = {}

with open(data) as f:
    contenido = json.load(f)


for i in contenido:
    if('RtkFlag' in i):
        if(i['RtkFlag'] not in rtkflags):
            rtkflags[i["RtkFlag"]] = 1
        else:
            rtkflags[i["RtkFlag"]] += 1
    if('Model' in i):
        if(i['Model'] not in cameramodels):
            cameramodels[i["Model"]] = 1
        else:
            cameramodels[i["Model"]] += 1


with open(r"C:\export.json", "w") as outfile:
    rtkflags.update(cameramodels)
    json.dump(rtkflags, outfile)
