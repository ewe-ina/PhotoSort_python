# PhotoSort_python
Python script to organize photos based on the date and time the photo was taken, using EXIF data.
#### Video Demo:
## Description
The script searches for graphic files in a given location, sorts them into appropriate directories and changes names based on the date and time the photo was taken using EXIF data

Directory tree name format: YYYY/YYYYMMDD/YYYYMMDD 
<br/>
File name format: YYYYMMDD_HHMMSS.EXT

## Usage
Clone repository.
<br/>
The script requires exiftool.exe to work properly. Download it from https://exiftool.org/ and place in the same directory as the script.
<br/>
Other requirements can be found in [requirements.txt](https://github.com/ewe-ina/PhotoSort_python/blob/main/requirements.txt). Install them using a terminal or a command prompt (navigate to the directory with script):
```console
pip install -r requirements.txt
```
Script is ready for use:
```console
python3 PhotoSort.py
```
