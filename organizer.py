# organizer.py

# Import the argparse module to handle command-line arguments.
# This will allow us to specify the target directory when we run the script.
import argparse
import sys
import logging
import shutil

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
    logging.info(f"organizing in source_path" )
    for item in source_path.iterdir():
        if item.is_file():
            file_extension = item.suffix
            print(f"foundfile : {item.name} extension :{file_extension}")
            destination_folder_name = 'Other'

            for category , extension in FILE_TYPE_MAP.items():
                if file_extension in extension:
                    destination_folder_name = category
                    break
            destination_dir = source_path / destination_folder_name

            destination_dir.mkdir(parents=True, exist_ok=True)

            destination_file_path = destination_dir/item.name
            counter = 1 
            while destination_file_path.exists():
                logging.warning(f"Conflict '{destination_file_path}' already exists")
                new_filename = f"{item.stem}({counter}){item.suffix}"
                destination_file_path = destination_dir/new_filename
                counter +=1


            try:
                shutil.move(item , destination_file_path)
                logging.INFO(f"file {item.name} destination {destination_dir}")
            except (FileExistsError , PermissionError) as e:
                logging.error(f"Could not move the '{item.name}' , Error: {e}") 
            except Exception as e:
                logging.error("an unexpected error occured while processing '{item.name}', error : {e}")









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="organize the files")
    parser.add_argument('source' ,help = 'path to mess' )
    args = parser.parse_args()
    source_path = pathlib.Path(args.source)

    logging.basicConfig(
        level= logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s ',
        handlers= [
            logging.FileHandler("organizer.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    org_dir(source_path)
    if not source_path.exists() or not source_path.is_dir():
        print(f"error:'{source_path}'does not exists or is not a directory")
        sys.exit(1)

    print("org in :",source_path)

