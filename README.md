# exif-rtk-data
The script calculates the number of images taken by each UAV (according to its camera model) and determines the RTK status in those where said measurement method was used, using ExifTool. The processing result is exported in json format.

RTK Flag identifies the status of RTK: 0-no positioning, 16-point positioning mode, 34-RTK floating point solution, 50-RTK fixed solution.
When the value of the status bit is 50, it is in the RTK fixed solution state, and the positioning accuracy is the highest at this time.


# How to Use
- Download exiftool.exe from https://exiftool.org/.
- Download ffmpeg.exe from https://ffmpeg.org/.
- Agregar la ruta a la variable de entorno PATH.
- pip install ffmpeg-python.
- pip install PyExifTool.


# List of correspondences between the UAV and the camera model:
- DJI AIR 2S - FC3411
- DJI MINI 2 - FC7303
- MAVIC MINI - FC7203
- MAVIC 2 PRO - L1D-20C
- MAVIC AIR - FC2103
- MAVIC AIR 2 - FC2204
- MAVIC PRO - FC220
- SPARK - FC1102
- PHANTOM 4 PRO - FC6310
- PHANTOM 4 PRO V2 - FC6310S
- PHANTOM 4 ADVANCED - FC6310
- PHANTOM 4 - FC330
- PHANTOM 4 RTK - FC6310R
- PHANTON 3 - FC300C
- PHANTOM 3 PRO - FC300S - FC300X
- PHANTOM 3 ADVANCED - FC300XW
- PHANTOM 3 STANDARD - FC300C
- PHANTOM 3 4K - FC300X
- PHANTOM 3 SE - FC300S
- INSPIRE 2 - FC6520 (ZenMuse X5S), FC6510 (X4S), X7S
- INSPIRE 1 SERIES - FC350