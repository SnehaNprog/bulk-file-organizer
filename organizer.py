# organizer.py

# Import the argparse module to handle command-line arguments.
# This will allow us to specify the target directory when we run the script.
import argparse

# Import the pathlib module to work with file system paths in an object-oriented way.
# This makes path manipulation more intuitive and cross-platform compatible.
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="organize the files")
    parser.add_argument('source' ,help = 'path to mess' )
