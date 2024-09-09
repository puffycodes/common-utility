# file: list_duplicate_files.py

import argparse
from common_util.file_util.file_index import FileIndex

def list_duplicate_files(dirname_list, pattern='*',
                         by='digest', include_hidden=False, verbose=False):
    if verbose:
        print(f'dirname_list: {dirname_list}')
        print(f'pattern: {pattern}')

    index_type_list = {
        'digest': FileIndex.INDEX_DIGEST,
        'filename': FileIndex.INDEX_FILENAME
    }

    index_type = index_type_list.get(by, FileIndex.INDEX_DIGEST)
    indexes = FileIndex(index_type=index_type)
    for dirname in dirname_list:
        indexes.add_from_directory(
            dirname, pattern=pattern, include_hidden=include_hidden,
            verbose=verbose
        )

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
                        help='name of directory to check for files')
    parser.add_argument('-p', '--pattern', default='*',
                        help='pattern of files to include')
    parser.add_argument('-a', '--include_hidden', action='store_true', default=False,
                        help='include hidden files')
    parser.add_argument('-b', '--by', choices=['digest', 'filename'],
                        default='digest',
                        help='attribute to determine duplication')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='show more information while running')
    args = parser.parse_args()

    list_duplicate_files(
        args.dirname, pattern=args.pattern,
        by=args.by, include_hidden=args.include_hidden, verbose=args.verbose
    )

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
