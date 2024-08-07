# file: file_index.py

import os
import hashlib
from common_util.dir_util import DirectoryUtility
from common_util.container.multi_level_index import MultiLevelIndex

class FileIndex:

    def __init__(self):
        self.max_level = 5
        self.indexes = MultiLevelIndex(max_level=self.max_level)
        return
    
    def add_from_directory(self, dirname, pattern='*', verbose=False):
        file_list = DirectoryUtility.list_files(
            dirname, pattern, recursive=True, get_relative_path=True
        )
        for file in file_list:
            full_path = os.path.join(dirname, file)
            digest = self.get_file_md5_hash(full_path)
            file_size = self.get_file_size(full_path)
            self.indexes.add(digest, (dirname, file, file_size))
            if verbose:
                print(f' - {file}: {file_size} {digest}')
        if verbose:
            print('=======')
        return

    def get_duplicate_file_list(self, verbose=False):
        duplicate_file_list = []
        for digest, value in self.indexes.iterate_entry():
            count = len(value)
            if count >= 2:
                duplicate_file_list.append((count, digest, value))
            if verbose:
                print(f'({count}) {digest}: {value}')
        return duplicate_file_list

    def get_file_md5_hash(self, file_name):
        with open(file_name, 'rb') as fd:
            data = fd.read()
            data_hash = hashlib.md5(data)
            digest = data_hash.hexdigest()
        return digest

    def get_file_size(self, file_name):
        file_size = os.path.getsize(file_name)
        return file_size

# --- end of file --- #
