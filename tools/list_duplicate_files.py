# file: list_duplicate_files.py

import os
import argparse
import hashlib
from common_util.dir_util import DirectoryUtility
from common_util.container.multi_level_index import MultiLevelIndex

def list_duplicate_files(dir_list, verbose=False):
    if verbose:
        print(dir_list)

    indexes = MultiLevelIndex(max_level=5)
    for dir in dir_list:
        file_list = DirectoryUtility.list_files(dir, '*', recursive=True, get_relative_path=True)
        for file in file_list:
            full_path = os.path.join(dir, file)
            digest = get_file_md5_hash(full_path)
            file_size = get_file_size(full_path)
            indexes.add(digest, (dir, file, file_size))
            if verbose:
                print(f' - {file}: {file_size} {digest}')
        if verbose:
            print('=======')

    duplicate_file_list = []
    for digest, value in indexes.iterate_entry():
        count = len(value)
        if count >= 2:
            duplicate_file_list.append((count, digest, value))
        if verbose:
            print(f'({count}) {digest}: {value}')
                
    return duplicate_file_list

def get_file_md5_hash(file_name):
    with open(file_name, 'rb') as fd:
        data = fd.read()
        data_hash = hashlib.md5(data)
        digest = data_hash.hexdigest()
    return digest

def get_file_size(file_name):
    file_size = os.path.getsize(file_name)
    return file_size

def main():
    parser = argparse.ArgumentParser(
        prog='list_duplicate_files',
        description='Show a list of duplicate files in directories'
    )
    parser.add_argument('dirnames', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()

    duplicate_file_list = list_duplicate_files(args.dirnames, verbose=args.verbose)
    print(f'Result:')
    for count, digest, value in duplicate_file_list:
        print(f'** ({count}): {digest}')
        for v in value:
            print(f'    - {v}')

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
