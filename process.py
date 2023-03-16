import json
import os
import sys
import tempfile
import exiftool
import ffmpeg


IMAGE_EXTENSIONS = ('.jpg', '.jpeg')
PARAMS = ["Rtkflag", "Model"]
TMP_FOLDER = tempfile.gettempdir()



def check_value_in_dict(tag_dict, tag_key, count_dict):
    '''
    Check if the tag value is in the dictionary or not. 
    If it's in the dict, increments its occurrence, 
    otherwise adds it for the first time
    '''
    count_dict[tag_dict[tag_key]] = 1 if tag_dict[tag_key] not in count_dict else count_dict[tag_dict[tag_key]] + 1



try:
    for arg in sys.argv[1:]:

        
        rtk_flag_count = {}
        no_rtk_count = {}
        rtk_model_count = {}
        total_count = {}
        num_files = 0
        is_image = False
        
        ext = os.path.splitext(arg)[1]

        
        if os.path.isdir(arg):
            for subdir, _, files in os.walk(arg):
                for file in files:
                    file_path = os.path.join(subdir, file)
                    if os.path.splitext(file)[1].lower() in IMAGE_EXTENSIONS:
                        is_image = True
                        with exiftool.ExifToolHelper() as et: 
                            metadata_dict = et.get_tags([file_path], PARAMS)
                            for tag_dict in metadata_dict:
                                if 'XMP:RtkFlag' in tag_dict:
                                    check_value_in_dict(tag_dict, "XMP:RtkFlag", rtk_flag_count)
                                    rtk_model_count[tag_dict["EXIF:Model"]] = rtk_flag_count
                                elif("EXIF:Model" in tag_dict):
                                    check_value_in_dict(tag_dict, "EXIF:Model", no_rtk_count)

                            num_files += len(metadata_dict)

        if os.path.splitext(arg)[1].lower() in ('.mp4', '.mov'):
            print(f"We have detected a file with extension {ext}")
            srt_file_name = input(f"Ingrese el nombre del archivo SRT: ")
            stream = ffmpeg.input(arg)
            stream = ffmpeg.output(stream, f'{srt_file_name}.SRT')
            ffmpeg.run(stream)

        if is_image:
            json_file_name = input(f"Enter the name of the JSON file: ")
            with open(os.path.join('.', f"{json_file_name}.json"), "w") as outfile:
                total_count["TOTAL"] = num_files
                rtk_model_count.update(no_rtk_count)
                rtk_model_count.update(total_count)
                json.dump(rtk_model_count, outfile)

except IndexError:
    print("No file dropped")