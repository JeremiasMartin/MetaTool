import json
import tempfile
import exiftool
from os import walk, sep, path
import sys

tmp_folder = tempfile.gettempdir()


def checkValueInDict(i, string, dictionary):
    '''
    Check if the value is in the dictionary or not. If it's in the dict, increments its occurrence, otherwise adds it for the first time
    '''
    dictionary[i[string]
               ] = 1 if i[string] not in dictionary else dictionary[i[string]]+1


rtk = {}
noRTK = {}
rtkflag = {}

extensions = ['.JPG', '.jpg', '.JPEG', '.jpeg']

params = ["Rtkflag", "Model"]

try:

    for arg in sys.argv[1:]:
        root_path = arg
        folder = root_path.split(sep)[-1]

        for subdir, dirs, files in walk(root_path):
            for file in files:
                filepath = subdir + sep + file
                print('{} processing...'.format(file))
                if(path.splitext(file)[1] in extensions):
                    with exiftool.ExifToolHelper() as et:
                        metadata = et.get_tags(filepath, params)
                        for d in metadata:
                            if 'XMP:RtkFlag' in d:
                                checkValueInDict(d, "XMP:RtkFlag", rtkflag)
                                rtk[d["EXIF:Model"]] = rtkflag
                            elif("EXIF:Model" in d):
                                checkValueInDict(d, "EXIF:Model", noRTK)

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
