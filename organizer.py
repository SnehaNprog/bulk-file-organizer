# organizer.py

# Import the argparse module to handle command-line arguments.
# This will allow us to specify the target directory when we run the script.
import argparse

# Import the pathlib module to work with file system paths in an object-oriented way.
# This makes path manipulation more intuitive and cross-platform compatible.
import pathlib
FILE_TYPE_MAP = {
    "Images" : ['.jpeg','.jpg','.png','.gif','.svg'],
    "Documents" : ['.pdf', '.docx','.txt','.xlsx','.srt'],
    "Audio" : ['.mp3','.wav','.aac'],
    "Video":['.mp4','.mov','.avi','.mkv'],
    "Archives":['.zip','.rar','.tar','.gz','.tar'],
    "Other":[]
}
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="organize the files")
    parser.add_argument('source' ,help = 'path to mess' )
    args = parser.parse_args()
    print("org in :",args.source)
