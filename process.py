import json
import tempfile
import exiftool
import os
import sys
import ffmpeg

# Utiliza variables en lugar de valores constantes
EXTENSIONS = ('.JPG', '.jpg', '.JPEG', '.jpeg')
PARAMS = ["Rtkflag", "Model"]
TMP_FOLDER = tempfile.gettempdir()


def check_value_in_dict(i, string, dictionary):
    '''
    Check if the value is in the dictionary or not. If it's in the dict, increments its occurrence, otherwise adds it for the first time
    '''
    dictionary[i[string]] = 1 if i[string] not in dictionary else dictionary[i[string]] + 1


try:
    for arg in sys.argv[1:]:
        root_path = arg
        folder = os.path.basename(root_path)

        rtkflag = {}
        no_rtk = {}
        rtk = {}
        total = {}
        cont = 0
        
        for subdir, dirs, files in os.walk(root_path):

            for file in files:

                filepath = os.path.join(subdir, file)
                ext = os.path.splitext(file)[1]

                if ext in EXTENSIONS:

                    with exiftool.ExifToolHelper() as et:

                        metadata = et.get_tags([filepath], PARAMS)

                        for d in metadata:

                            if 'XMP:RtkFlag' in d:
                                check_value_in_dict(d, "XMP:RtkFlag", rtkflag)
                                rtk[d["EXIF:Model"]] = rtkflag

                            elif("EXIF:Model" in d):
                                check_value_in_dict(d, "EXIF:Model", no_rtk)

                        cont += len(metadata)

                elif ext in ('.MP4', '.MOV'):
                    print(f"Hemos detectado un archivo con extensión {ext}")
                    filename_output = os.path.splitext(file)[0]
                    output_path = os.path.join(TMP_FOLDER, f'{filename_output}.SRT')
                    stream = ffmpeg.input(filepath)
                    stream = ffmpeg.output(stream, output_path)
                    ffmpeg.run(stream)

        filename_output = input(f"Ingrese el nombre del archivo json para la carpeta {folder}: ")
        with open(os.path.join('.', f"{filename_output}.json"), "w") as outfile:
            total["TOTAL"] = cont
            rtk.update(no_rtk)
            rtk.update(total)
            json.dump(rtk, outfile)

except IndexError:
    print("No file dropped")

