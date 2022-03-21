import subprocess
import json
import sys
import tempfile

tmp_folder = tempfile.gettempdir()
exiftool_exe = '.\exiftool.exe'
# ffmpeg = '.\ffmpeg.exe' next impl
tmp_output = f'{tmp_folder}\data.json'


def checkDictionary(i, string, dictionary):

    dictionary[i[string]
               ] = 1 if i[string] not in dictionary else dictionary[i[string]]+1


rtkflag = {}
noRTK = {}
rtk = {}
total = {}
cont = 0

try:
    sys.argv[1]
    filename_output = input(
        "Ingrese el nombre del archivo y presione ENTER: ")

    with open(f".\{filename_output}.json", "w") as outfile:
        for arg in sys.argv[1:]:
            root_path = arg

            # Generating json file using exiftool (RtkFlag - cameraModel)
            exiftool_command = [exiftool_exe, root_path,
                                '-rtkflag', '-Model', '-q', '-json', '-fast', '-r', '-ext', 'JPG', '-ext', 'jpg', '-ext', 'jpeg', '-ext', 'JPEG']  # https://www.exiftool.org/exiftool_pod.html#OPTIONS

            with open(tmp_output, "w") as f:
                subprocess.run(exiftool_command, stdout=f)

            with open(tmp_output) as f:
                contenido = json.load(f)

            for i in contenido:
                if('RtkFlag' in i):
                    checkDictionary(i, "RtkFlag", rtkflag)
                    rtk[i["Model"]] = rtkflag
                elif('Model' in i):
                    checkDictionary(i, "Model", noRTK)
            cont += len(contenido)

        total["TOTAL"] = cont
        rtk.update(noRTK)
        rtk.update(total)
        json.dump(rtk, outfile)

except IndexError:
    print("No file dropped")
