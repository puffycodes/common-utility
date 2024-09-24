# file: file_index.py

'''
Containers that stores file information
'''

import os
import hashlib
from common_util.dir_util import DirectoryUtility
from common_util.container.multi_level_index import MultiLevelIndex

class FileIndex:
    '''
    A container that stores file information indexes by either file hashes
    or file names.
    '''

    # - Subkey Generators for FileIndex Class

    class SubkeyGeneratorUsingFilename(MultiLevelIndex.SubkeyGenerator):
        '''
        A subkey generator that uses a file name to generate the subkey.
        '''

        def __init__(self, empty_subkey='none', use_file_extension=True):
            super().__init__(empty_subkey=empty_subkey)
            self.use_file_extension = use_file_extension
            return
        
        def get_subkey(self, key, level):
            self.check_level(key, level)
            subkey = self.empty_subkey
            basename = os.path.basename(key)
            name, extension = self.get_name_and_extension(basename)
            if self.use_file_extension == True:
                if level == 0:
                    if extension != '':
                        subkey = extension
                    else:
                        subkey = self.empty_subkey
                else:
                    # subkey = self.get_subkey_from_name(name, level-1)
                    subkey = self.get_subkey_from_string(name, level-1)
            else:
                # subkey = self.get_subkey_from_name(name, level)
                subkey = self.get_subkey_from_string(name, level)
            return subkey
        
        # def get_subkey_from_name(self, name, level):
        #     subkey = self.empty_subkey
        #     if len(name) > level:
        #         subkey = name[level]
        #     return subkey
        
        def get_name_and_extension(self, filename):
            filename_parts = filename.split('.')
            component_count = len(filename_parts)
            if component_count <= 0:
                # empty string
                name, extension = '', ''
            elif component_count == 1:
                # no extension
                name, extension = filename_parts[0], ''
            else:
                name, extension = filename_parts[0], filename_parts[-1]
            return name, extension
        
    # - FileIndex Class

    INDEX_DIGEST = 0
    INDEX_FILENAME = 1
        
    def __init__(self, index_type=INDEX_DIGEST):
        self.max_level = 5
        self.index_type = index_type
        if self.index_type == FileIndex.INDEX_FILENAME:
            self.key_generator = FileIndex.SubkeyGeneratorUsingFilename(
                empty_subkey='none', use_file_extension=True
            )
        else:
            # default to using digest
            self.index_type = FileIndex.INDEX_DIGEST
            self.key_generator = MultiLevelIndex.SubkeyGeneratorUsingHash(
                empty_subkey = 'none'
            )
        self.indexes = MultiLevelIndex(
            max_level=self.max_level, key_generator=self.key_generator
        )
        return
    
    def add_file(self, dirname, file, verbose=False):
        full_path = os.path.join(dirname, file)
        digest = self.get_file_md5_hash(full_path)
        file_size = self.get_file_size(full_path)
        if self.index_type == FileIndex.INDEX_FILENAME:
            data_item_key = os.path.basename(full_path)
        else:
            data_item_key = digest
        data_item = self.create_data_item(dirname, file, file_size, digest)
        self.indexes.add(data_item_key, data_item)
        if verbose:
            print(f' - {file}: {file_size} {digest}')
        return
    
    def add_from_directory(self, dirname, pattern='*', include_hidden=False,
                           verbose=False):
        file_list = DirectoryUtility.list_files(
            dirname, pattern, recursive=True, get_relative_path=True,
            include_hidden=include_hidden
        )
        for file in file_list:
            self.add_file(dirname, file, verbose=verbose)
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
    
    # --- Internal Functions

    def get_file_md5_hash(self, file_name):
        with open(file_name, 'rb') as fd:
            data = fd.read()
            data_hash = hashlib.md5(data)
            digest = data_hash.hexdigest()
        return digest

    def get_file_size(self, file_name):
        file_size = os.path.getsize(file_name)
        return file_size
    
    def create_data_item(self, dirname, file, file_size, digest):
        return (dirname, file, file_size, digest)

# --- end of file --- #
