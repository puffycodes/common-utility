# file: list_duplicate_files.py

import os
import argparse
import hashlib
from common_util.dir_util import DirectoryUtility
from common_util.container.multi_level_index import MultiLevelIndex
from common_util.file_util.file_index import FileIndex

def list_duplicate_files(dirname_list, verbose=False):
    if verbose:
        print(dirname_list)

    indexes = FileIndex()
    for dirname in dirname_list:
        indexes.add_from_directory(dirname, verbose=verbose)

    duplicate_file_list = indexes.get_duplicate_file_list(verbose=verbose)

    print(f'Result:')
    for count, digest, value in duplicate_file_list:
        print(f'** ({count}): {digest}')
        for v in value:
            print(f'    - {v}')

    return

def main():
    parser = argparse.ArgumentParser(
        prog='list_duplicate_files',
        description='Show a list of duplicate files in directories'
    )
    parser.add_argument('dirname', nargs='+',
                        help='name of directory to check')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='show more information while running')
    args = parser.parse_args()

    list_duplicate_files(args.dirname, verbose=args.verbose)

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
