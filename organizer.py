# organizer.py

# Import the argparse module to handle command-line arguments.
# This will allow us to specify the target directory when we run the script.
import argparse
import sys

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


def org_dir(source_path : pathlib.Path):
    print(f'organizing files in {source_path}')
    for item in source_path.iterdir():
        if item.is_file():
            file_extension = item.suffix
            print(f"foundfile : {item.name} extension :{file_extension}")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="organize the files")
    parser.add_argument('source' ,help = 'path to mess' )
    args = parser.parse_args()
    source_path = pathlib.Path(args.source)
    org_dir(source_path)
    if not source_path.exists() or not source_path.is_dir():
        print(f"error:'{source_path}'does not exists or is not a directory")
        sys.exit(1)

    print("org in :",source_path)

