#modular docstring explain what a certain module or file does , this one org the path u give it 
#in different folders , you can prog it externally with config.json 

import argparse
import sys
import logging
import shutil
import json
import pathlib

from tqdm import tqdm


def load_config(config_path:pathlib.Path):


    """
    Loads and validates the organization rules from a JSON configuration file.

    This function attempts to open and parse the specified JSON file. It handles
    potential FileNotFoundError and json.JSONDecodeError, logging helpful
    error messages and exiting the script if the configuration is invalid or missing.
    Args:
    config_path (pathlib.Path): The path to the config.json file.
    Returns:
    dict: A dictionary containing the file type mappings.
    """
    
    try:
        with open (config_path, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except FileNotFoundError:
        logging.error(f"config file not found at '{config_path}'")
        sys.exit(1)
    except json.JSONDecodeError as e :
        logging.error(f"the config contains invalid json '{e}'")
        sys.exit(1)


def process_file(item : pathlib.Path ,FILE_TYPE_MAP :dict , dry_run : bool , source_path : pathlib.Path  ):

    """
    Processes a single file: determines its destination and moves it or simulates the move.

    This function is the core worker of the organization process. It finds the
    appropriate category for the file based on its extension, handles potential
    filename conflicts by renaming the file if necessary, and performs the
    actual move operation with error handling.

    Args:
        file_path (pathlib.Path): The path to the file to be processed.
        source_path (pathlib.Path): The root directory where organization is happening.
        file_type_map (dict): The dictionary of organization rules.
        dry_run (bool): If True, simulate the file move; otherwise, perform it.
    """
    file_extension = item.suffix
    print(f"foundfile : {item.name} extension :{file_extension}")
    destination_folder_name = 'Other'
    for category , extension in FILE_TYPE_MAP.items():
                if file_extension in extension:
                    destination_folder_name = category
                    break
    destination_dir = source_path / destination_folder_name
    if dry_run:
                destination_file_path = destination_dir/item.name
                logging.info(f"dry run would move '{item.name}' to '{destination_file_path}'")
    else:
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
    
    


    

def org_dir(source_path : pathlib.Path , dry_run:bool , FILE_TYPE_MAP:dict):

    """
    Orchestrates the file organization process for a given directory.

    This function serves as the main entry point for the organization logic.
    It announces the operational mode (dry run or live), discovers all files
    in the source directory, and then delegates the processing of each file
    to the process_file function.

    Args:
        source_path (pathlib.Path): The directory to be organized.
        dry_run (bool): If True, simulate without moving files.
        file_type_map (dict): A dictionary mapping folder names to file extensions.
    """


    logging.info(f"organizing in source_path" )
    if dry_run:
        logging.info("--Dry_Run mode enabled no files will be moved")
    else:
        logging.warning("live mode chnages will be made")

    files_to_process = [item for item in source_path.iterdir() if item.is_file()]
    for item in tqdm(files_to_process , desc= "organizing files"):
         process_file(item , FILE_TYPE_MAP ,dry_run , source_path )




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="organize the files")
    parser.add_argument('source' ,help = 'path to mess' )
    parser.add_argument('--dry-run',action= 'store_true',help='Stimulate the org without moving the file')
    args = parser.parse_args()

    config_file_path = pathlib.Path(__file__).parent/"config.json"
    file_type_map_from_config = load_config(config_file_path)

    source_path = pathlib.Path(args.source)

    logging.basicConfig(
        level= logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s ',
        handlers= [
            logging.FileHandler("organizer.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    if not source_path.exists() or not source_path.is_dir():
        print(f"error:'{source_path}'does not exists or is not a directory")
        sys.exit(1)
    
    org_dir(source_path , args.dry_run , file_type_map_from_config )

    print("org in :",source_path)

