from os import sep
import subprocess
import json
import sys
import tempfile

tmp_folder = tempfile.gettempdir()
exiftool_exe = '.\exiftool.exe'
tmp_output = f'{tmp_folder}\data.json'


def checkDictionary(i, string, dictionary):

    dictionary[i[string]
               ] = 1 if i[string] not in dictionary else dictionary[i[string]]+1


rtkflag = {}
noRTK = {}
rtk = {}

try:

    for arg in sys.argv[1:]:
        root_path = arg
        folder = root_path.split(sep)[-1]

        # Generating json file using exiftool (RtkFlag - cameraModel)
        exiftool_command = [exiftool_exe, root_path,
                            '-rtkflag', '-Model', '-q', '-json', '-fast', '-r', '-ext', 'JPG', '-ext', 'jpg','-ext','jpeg', '-ext', 'JPEG']  # https://www.exiftool.org/exiftool_pod.html#OPTIONS

        with open(tmp_output, "w") as f:
            process = subprocess.run(exiftool_command, stdout=f)

        with open(tmp_output) as f:
            contenido = json.load(f)

        for i in contenido:
            if('RtkFlag' in i):
                checkDictionary(i, "RtkFlag", rtkflag)
                rtk[i["Model"]] = rtkflag
            elif('Model' in i):
                checkDictionary(i, "Model", noRTK)

        filename_output = input(
            f"Ingrese el nombre del archivo json para la carpeta {folder}: ")

        with open(f".\{filename_output}.json", "w") as outfile:
            rtk.update(noRTK)
            json.dump(rtk, outfile)

        rtk.clear()
        rtkflag.clear()
        noRTK.clear()

except IndexError:
    print("No file dropped")
