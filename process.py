import subprocess
import json
import sys
import tempfile
import ffmpeg
import os


TEMP_FOLDER = tempfile.gettempdir()
EXIFTOOL_EXE = '.\exiftool.exe'
TEMP_OUTPUT_FILE = f'{TEMP_FOLDER}\data.json'


def checkDictionary(i, string, dictionary):
    """
    Adds an entry to the dictionary, counting the number of times the key appears in the dictionary.
    """
    dictionary[i[string]] = 1 if i[string] not in dictionary else dictionary[i[string]]+1



# Dictionaries to store camera model and RTK flag counts
rtkflag = {}
noRTK = {}
rtk = {}
total = {}
cont = 0
img = False

try:

    sys.argv[1]
    filename_output = input("Enter the output filename and press ENTER: ")

    for arg in sys.argv[1:]:
        if(not(arg.endswith(".MOV") | arg.endswith(".MP4"))):
            img = True
            exiftool_command = [EXIFTOOL_EXE, arg, '-rtkflag', '-Model', '-q', '-json', '-fast', '-r', '-ext', 'JPG', '-ext', 'jpg', '-ext', 'jpeg', '-ext', 'JPEG']
            
            # Run the exiftool command and store the output in a temporary file
            with open(TEMP_OUTPUT_FILE, "w") as f:
                subprocess.run(exiftool_command, stdout=f)

            with open(TEMP_OUTPUT_FILE) as f:
                contenido = json.load(f)

            for data in contenido:
                if('RtkFlag' in data):
                    checkDictionary(data, "RtkFlag", rtkflag)
                    rtk[data["Model"]] = rtkflag
                elif('Model' in data):
                    checkDictionary(data, "Model", noRTK)
            cont += len(contenido)

        elif((arg.endswith(".MP4")) | arg.endswith(".MOV")):
            # If the file is an MP4 or MOV, convert it to SRT format
            print("We detected an MP4/MOV file.")
            stream = ffmpeg.input(arg)
            stream = ffmpeg.output(stream, f'{filename_output}.SRT')
            ffmpeg.run(stream)
        
        # Add the total count to the RTK dictionary
        total["TOTAL"] = cont
        rtk.update(noRTK)
        rtk.update(total)

    if(img):
        with open(os.path.join(".", f"{filename_output}.json"), "w") as outfile:
            json.dump(rtk, outfile)
    
except IndexError:
    print("No file dropped")