import os
import sys
import shutil
import re
import argparse

parser = argparse.ArgumentParser(description="""
Clean up your files 

The dafault script will create folders of all the extension types in the current
working directory and will move all files into their respective folders.

Example:
    - All files with the PNG file extension will be moved to a folder named png.
      Such folder will be in the current working directory.
""")
parser.add_argument('--copy', action="store_true",
                    help="Copies files to new folders instead")
parser.add_argument('--path', default=".", type=str,
                    help="Directory to clean up. Current working directory by default", required=False)
parser.add_argument(
    '--postfix', type=str, default="",
    help="Postfix that will be appended to extension type folder name. ie jpg_<postfix> or default jpg", required=False)


args = parser.parse_args()

# Operates on files and folders


class FileManager:
    def __init__(self, path):
        # Define working path
        self.path = path
        # Setup extension type set
        self.extension_types = set()
        # variable to associate extension type with extension folder
        self.extension_folders = dict()
        # Method to setup the extension type set
        self.setup_extension_type_set()

    def create_folders(self, postfix):
        # Method to set up the names for the folders
        self.setup_folder_names(postfix)
        # Create folders by the folder names
        for folder_path in self.extension_folders:
            try:
                os.mkdir(self.extension_folders[folder_path])
            except FileExistsError as error:
                print(f"{folder_path} folder already exists, ignoring...")

    def setup_folder_names(self, postfix):
        for ext in self.extension_types:
            # If the extension is not other create the folder with postfix name
            if "other" not in ext:
                self.extension_folders[ext] = f'{self.path}/{ext}{postfix}'
            else:  # other will not have a postfix
                self.extension_folders[ext] = f'{self.path}/{ext}'

    def move_files(self):
        with os.scandir(self.path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if re.search(r'\.', entry.name):
                        file_ext_combo = re.split(r'\.', entry.name)
                        if self.extension_folders.get(file_ext_combo[-1]):
                            if args.copy:
                                shutil.copy2(entry.name, self.extension_folders.get(
                                    file_ext_combo[-1]) + "/" + entry.name)
                            elif not args.copy:
                                shutil.move(entry.name, self.extension_folders.get(
                                    file_ext_combo[-1]) + "/" + entry.name)
                    else:  # this is if the file doesn't have an extension
                        if self.extension_folders.get('other'):
                            if args.copy:
                                shutil.copy2(entry.name, self.extension_folders.get('other'))
                            else:
                                shutil.move(entry.name, self.extension_folders.get('other'))

    # Set up extension set
    def setup_extension_type_set(self):
        with os.scandir(self.path) as it:
            # Create pattern to match
            period_pattern = re.compile(r'\.')
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    # In some instances a file may not contain an extension
                    # In other instances a file may have an extension greater than 3
                    # Find the last period position and extract extension till end of str
                    if re.search(period_pattern, entry.name):
                        # add name of extension to set
                        self.extension_types.add(re.split(period_pattern, entry.name, maxsplit=3)[-1])
                    # which we could consider such file to be under 'other'
                    else:
                        self.extension_types.add('other')

# Orchestrating class


class CleanUp:
    def __init__(self, path, postfix=""):
        try:
            # Change directory passed by client
            os.chdir(path)

        # If error output and exit
        except OSError as error:
            print(error)
            exit()
        else:
            # Save working dir as specified
            self.working_path = os.getcwd()

        # If postfix passed, assign
        self.postfix = "_" + postfix if postfix != "" else ""

    def organize(self):
        file_manager = FileManager(self.working_path)
        file_manager.create_folders(self.postfix)
        file_manager.move_files()


# Main flow
if __name__ == "__main__":
    cleanup = CleanUp(path=args.path, postfix=args.postfix)
    cleanup.organize()
