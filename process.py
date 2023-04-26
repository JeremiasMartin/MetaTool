import subprocess
import json
import sys
import tempfile
import ffmpeg
import os

TEMP_FOLDER = tempfile.gettempdir()
EXIFTOOL_EXE = 'bin\exiftool.exe'
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
mp4_files = False
try:

    print('''

 ****     ****           **               **********                    **
/**/**   **/**          /**              /////**///                    /**
/**//** ** /**  *****  ******  ******        /**      ******   ******  /**
/** //***  /** **///**///**/  //////**       /**     **////** **////** /**
/**  //*   /**/*******  /**    *******       /**    /**   /**/**   /** /**
/**   /    /**/**////   /**   **////**       /**    /**   /**/**   /** /**
/**        /**//******  //** //********      /**    //****** //******  ***
//         //  //////    //   ////////       //      //////   //////  /// 

''')

    for arg in sys.argv[1:]:
        if(os.path.isdir(arg)):
            mp4_files = [f for f in os.listdir(arg) if os.path.isfile(os.path.join(
                arg, f)) and (os.path.splitext(f)[1].lower() in ('.mp4', '.mov'))]
        if(mp4_files):
            for mp4_file in mp4_files:
                # If the file is an MP4, convert it to SRT format
                print(f"Processing file: {arg}")
                stream = ffmpeg.input(os.path.join(arg, mp4_file))
                stream = ffmpeg.output(stream, f'{os.path.join(".", (mp4_file).split(".")[0])}.srt')
                ffmpeg.run(stream)

        elif(not os.path.isdir(arg)) and (os.path.splitext(arg)[1].lower() in ('.mp4' or ".mov")):
            print(f"Processing file: {os.path.basename(arg)}")
            stream = ffmpeg.input(arg)
            stream = ffmpeg.output(stream, f'{os.path.splitext(arg)[0]}.srt')
            ffmpeg.run(stream)

        else:
            img = True
            exiftool_command = [EXIFTOOL_EXE, arg, '-rtkflag', '-Model', '-q', '-json',
                               '-fast', '-r', '-ext', 'JPG', '-ext', 'jpg', '-ext', 'jpeg', '-ext', 'JPEG', '-fast', '-m']
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
                print(f"Processed file: {data['SourceFile']}")
            cont += len(contenido)

        # Add the total count to the RTK dictionary
        total["TOTAL"] = cont
        rtk.update(noRTK)
        rtk.update(total)

    if(img):
        filename_output = input("Enter the output filename and press ENTER: ")
        with open(os.path.join(".", f"{filename_output}.json"), "w") as outfile:
            json.dump(rtk, outfile)
    input("Press Enter to Exit...")
            
except Exception as e:
    print("An error has ocurred:")
    print(e)
    input("Press Enter to Exit...")