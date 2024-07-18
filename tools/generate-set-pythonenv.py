# file: generate-set-pythonenv.py

import argparse
import os
import sys

def generate_windows_script(path_list, fout=sys.stdout):
    path_value = ';'.join(path_list)
    print(
f'''
@echo off
set PYTHONPATH={path_value}
''',
        file=fout, end=''
    )
    return

def generate_unix_script(path_list, fout=sys.stdout):
    path_value = ':'.join(path_list)
    print(
f'''
export PYTHONPATH={path_value}
''',
        file=fout, end=''
    )
    return

def main():
    parser = argparse.ArgumentParser(
        prog='generate-set-pythonenv',
        description='Generate a script that will set PYTHONENV'
    )
    parser.add_argument('pathname', nargs='+')
    parser.add_argument('--script_type',
                        choices=[ 'unix', 'windows' ], default='windows')
    args = parser.parse_args()

    outfile = sys.stdout
    errfile = sys.stderr

    path_list = []
    for path in args.pathname:
        full_path = os.path.abspath(os.path.join(path))
        path_list.append(full_path)
    if args.script_type == 'windows':
        generate_windows_script(path_list, fout=outfile)
    elif args.script_type ==  'unix':
        generate_unix_script(path_list, fout=outfile)
    else:
        print(f'unknown script type: {args.script_type}', file=errfile)

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
