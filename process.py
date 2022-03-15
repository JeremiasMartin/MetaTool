import json
import tempfile
import exiftool
from os import walk, sep, path
import sys

try:
    root_path = sys.argv[1]

    tmp_folder = f'{tempfile.gettempdir()}'
    export = r".\export.json"

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

    for subdir, dirs, files in walk(root_path):
        for file in files:
            filepath = subdir + sep + file
            if(path.splitext(file)[1] in extensions):
                with exiftool.ExifToolHelper() as et:
                    metadata = et.get_tags(filepath, params)
                    for d in metadata:
                        if 'XMP:RtkFlag' in d:
                            checkValueInDict(d, "XMP:RtkFlag", rtkflag)
                            rtk[d["EXIF:Model"]] = rtkflag
                        elif("EXIF:Model" in d):
                            checkValueInDict(d, "EXIF:Model", noRTK)

    with open(export, "w") as outfile:
        rtk.update(noRTK)
        json.dump(rtk, outfile)

except IndexError:
    print("No file dropped")
