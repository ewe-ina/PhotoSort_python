import exiftool
import json
import os
import PySimpleGUI as sg
from pathlib import Path
from shutil import copy2
from wcmatch import glob


def main():
    working_directory = os.getcwd()

    #sg.theme('DarkAmber')   # Window theme

    layout = [  [sg.Text('PhotoSort')],
                [sg.Text('Select source folder      '), sg.InputText(key="-SOURCE-", default_text=working_directory), sg.FolderBrowse(initial_folder=working_directory)],
                [sg.Text('Select destination folder'), sg.InputText(key="-DESTINATION-", default_text=f"{working_directory}"), sg.FolderBrowse(initial_folder=working_directory)],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('PhotoSort', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "Ok":
            source = Path(values["-SOURCE-"])
            destination = Path(values["-DESTINATION-"])
            print(f"Source folder: {source}")
            print(f"Destination folder: {destination}")
            break

    window.close()



    try:
        graphic_files = []
        graphic_files = get_graphic_files(source, graphic_files)
        print(graphic_files)

        for file in graphic_files:

            # return new name (absolute path) based on meta data
            new_file = get_new_name(file, destination)

            copy_and_rename(file, new_file)
            
            #source_file.rename(target)
    except Exception as e:
        print(f"exception: {e}")


# zwraca listę wszystkich plików graficznych z wszystkich folderów w głąb
def get_graphic_files(src, list):

    for item in os.listdir(src):
        current_path = os.path.join(src, item)

        if os.path.isdir(current_path):
            get_graphic_files(current_path, list)

    list.extend(glob.glob(f"{src}/*.@(jpg|jpeg|gif|png|raw)", flags=glob.EXTGLOB, root_dir=src))
    
    return list

# return new name (absolute path) based on meta data
# YYYY/YYYYMM/YYYYMMDD/yyyymmdd_timestamp.jpg
def get_new_name(file, dest):
    src_file = Path(file)

    extension = src_file.suffix

    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file)
        print(json.dumps(metadata, indent=2))
        print("__________________")
        print("SourceFile", metadata[0]["SourceFile"])
        print("EXIF:DateTimeOriginal", metadata[0]["EXIF:DateTimeOriginal"])
        print("EXIF:CreateDate", metadata[0]["EXIF:CreateDate"])
        print("File:FileCreateDate", metadata[0]["File:FileCreateDate"])
        print("File:FileModifyDate", metadata[0]["File:FileModifyDate"])
        print("__________________")
    
    date, time = metadata[0]["EXIF:DateTimeOriginal"].split(sep=" ")
    print(f"date {date}")
    print(f"time {time}")
    YYYY, MM, DD = date.split(sep=":")
    time = time.replace(":", "")

    YYYYMM = YYYY + MM
    YYYYMMDD = YYYY + MM + DD


    dest_file_name = f"{YYYYMMDD}_{time}{extension}"

    dest_file = dest / YYYY / YYYYMM / YYYYMMDD / dest_file_name
    print(dest_file)

    return dest_file
    

def copy_and_rename(src, dest):
    # Create folder if doesn't exist
    Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)

    # jeśli plik istnieje dodaj nr
    unique_dest = uniquify(dest)

    copy2(src, unique_dest)


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{filename}_{counter}{extension}"
        counter += 1

    return path


if __name__ == "__main__":
    main()
