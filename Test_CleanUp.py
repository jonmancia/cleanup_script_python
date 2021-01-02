import unittest
from random import choice
import re
import os
from CleanUp import CleanUp, FileManager


class CleanUpTests(unittest.TestCase):
    def setUp(self):
        os.chdir('/Users/jonathanmancia/Documents/Programming_Projects/test')
        self.exts = ('txt', 'py', 'doc', 'png', 'mp4')
        self.files_created = list()
        for num in range(15):
            file_name = f'test_file{num}.{choice(self.exts)}'
            with open(file_name, 'w'):
                self.files_created.append(file_name)

        self.filemanager = FileManager('.')

    def test_create_folders(self):
        ''' Testing the correct creation of folder names '''
        self.filemanager.create_folders('')

        with os.scandir() as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    self.assertIn(entry.name, self.exts)

    def test_move_files(self):
        self.filemanager.move_files()
        with os.scandir() as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    with os.scandir(entry.name) as itera:
                        for item in itera:
                            self.assertIn(item.name, filter(lambda x: entry.name in x, self.files_created))

    def tearDown(self):
        for item in self.files_created:
            os.remove(item)
        for item in self.exts:
            os.rmdir(item)


if __name__ == "__main__":
    unittest.main(verbosity=3)
