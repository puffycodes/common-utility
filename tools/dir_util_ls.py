# file: dir_util_ls.py

import sys
import argparse
import common_util.dir_util as dir

def list_files_in_directory(dirname, pattern,
                            recursive=False, include_hidden=False,
                            get_relative_path=False,
                            verbose=False, outfile=sys.stdout):
    files = dir.DirectoryUtility.list_files(
        dirname, pattern,
        recursive=recursive, include_hidden=include_hidden,
        get_relative_path=get_relative_path, verbose=verbose
    )
    print(f'directory: {dirname}', file=outfile)
    for file in files:
        print(f' {file}', file=outfile)
    print(file=outfile)
    return

def list_subdirectories_in_directory(dirname, pattern,
                                     recursive=False, include_hidden=False, 
                                     get_relative_path=False,
                                     verbose=False, outfile=sys.stdout):
    subdirs = dir.DirectoryUtility.list_subdirectories(
        dirname, pattern,
        recursive=recursive, include_hidden=include_hidden,
        get_relative_path=get_relative_path, verbose=verbose
    )
    print(f'directory {dirname}', file=outfile)
    for subdir in subdirs:
        print(f' {subdir}', file=outfile)
    print(file=outfile)
    return

def main():
    parser = argparse.ArgumentParser(
        prog='dir_util_ls',
        description='List files or subdirectories in the given list of directories.'
    )
    parser.add_argument('dirname', nargs='+',
                        help='directory name to list')
    parser.add_argument('-p', '--pattern', default='*',
                        help='pattern of the files or directories to list')
    #parser.add_argument('-o', '--outfile')
    parser.add_argument('-d', '--directory_only', action='store_true', default=False,
                        help='list directories instead of files')
    parser.add_argument('-r', '--recursive', action='store_true', default=False,
                        help='list recursively into subdirectories')
    parser.add_argument('--include_hidden', action='store_true', default=False,
                        help='list hidden files')
    parser.add_argument('-R', '--get_relative_path', action='store_true', default=False,
                        help='output relative path instead of full path')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='display more information while listing')
    args = parser.parse_args()

    if args.directory_only:
        for dirname in args.dirname:
            list_subdirectories_in_directory(
                dirname, args.pattern,
                recursive=args.recursive, include_hidden=args.include_hidden,
                get_relative_path=args.get_relative_path,
                verbose=args.verbose
            )
    else:
        for dirname in args.dirname:
            list_files_in_directory(
                dirname, args.pattern,
                recursive=args.recursive, include_hidden=args.include_hidden,
                get_relative_path=args.get_relative_path, 
                verbose=args.verbose
            )
    
    return

if __name__ == '__main__':
    main()

# --- end of file --- #
