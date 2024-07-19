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

def generate_posix_script(path_list, fout=sys.stdout):
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
        description='Generate a script that will set PYTHONPATH to the given paths.'
    )
    parser.add_argument('pathname', nargs='+',
                        help='path to add to the variable PYTHONPATH')
    parser.add_argument('--script_type',
                        choices=[ 'posix', 'windows', 'auto' ], default='auto',
                        help='the os for which the script is used for')
    args = parser.parse_args()

    fout = sys.stdout
    ferr = sys.stderr

    path_list = []
    for path in args.pathname:
        full_path = os.path.abspath(os.path.join(path))
        path_list.append(full_path)

    if args.script_type == 'windows':
        generate_windows_script(path_list, fout=fout)
    elif args.script_type ==  'posix':
        generate_posix_script(path_list, fout=fout)
    elif args.script_type == None or args.script_type == '' or args.script_type == 'auto':
        os_name = os.name
        if os_name == 'posix' or os_name == 'java':
            generate_posix_script(path_list, fout=fout)
        elif os_name == 'nt':
            generate_windows_script(path_list, fout=fout)
        else:
            print(f'Error: unknown os name: {os_name}', file=ferr)
    else:
        print(f'Error: unknown script type: {args.script_type}', file=ferr)

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
