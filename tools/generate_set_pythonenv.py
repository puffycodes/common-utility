# file: generate_set_pythonenv.py

import argparse
import os
import sys
import re

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

def read_paths_from_script(fin=sys.stdin):
    windows_regex = r'^set PYTHONPATH=(.*)$'
    posix_regex = r'^export PYTHONPATH=(.*)$'
    path_list = []
    lines = fin.readlines()
    for line in lines:
        group = re.match(windows_regex, line, flags=re.IGNORECASE)
        if group != None:
            curr_paths = group[1].split(';')
            path_list.extend(curr_paths)
            continue
        group = re.match(posix_regex, line, flags=re.IGNORECASE)
        if group != None:
            curr_paths = group[1].split(':')
            path_list.extend(curr_paths)
            continue
    return path_list

def mismatch_warning(script_type, os_name, ferr=sys.stderr):
    print(
        f'Warning: script type ({script_type}) generated on this os ({os_name}) may not work correctly',
        file=ferr
    )
    return

def generate_script(path_list, script_type, filenames=[],
                    fout=sys.stdout, ferr=sys.stderr):
    abs_path_list = []

    for filename in filenames:
        with open(filename, 'r') as fd:
            curr_paths = read_paths_from_script(fin=fd)
        for path in curr_paths:
            abs_path = os.path.abspath(os.path.join(path))
            if abs_path not in abs_path_list:
                abs_path_list.append(abs_path)

    for path in path_list:
        abs_path = os.path.abspath(os.path.join(path))
        if abs_path not in abs_path_list:
            abs_path_list.append(abs_path)

    os_name = os.name
    if script_type == 'windows':
        if os_name != 'nt':
            mismatch_warning(script_type, os_name)
        generate_windows_script(abs_path_list, fout=fout)
    elif script_type ==  'posix':
        if os_name != 'posix' and os_name != 'java':
            mismatch_warning(script_type, os_name)
        generate_posix_script(abs_path_list, fout=fout)
    elif script_type == None or script_type == '' or script_type == 'auto':
        if os_name == 'posix' or os_name == 'java':
            generate_posix_script(abs_path_list, fout=fout)
        elif os_name == 'nt':
            generate_windows_script(abs_path_list, fout=fout)
        else:
            print(f'Error: unknown os name: {os_name}', file=ferr)
    else:
        print(f'Error: unknown script type: {script_type}', file=ferr)

    return

def main():
    parser = argparse.ArgumentParser(
        prog='generate_set_pythonenv',
        description='Generate a script that will set PYTHONPATH to the given paths.'
    )
    parser.add_argument('--pathname', '-p', nargs='+', default=[],
                        help='path to add to the variable PYTHONPATH')
    parser.add_argument('--include_file', '-i', nargs='+', default=[],
                        help='an existing script file to read paths from')
    parser.add_argument('--script_type', '-s',
                        choices=[ 'posix', 'windows', 'auto' ], default='auto',
                        help='the os for which the script is used for')
    args = parser.parse_args()

    fout = sys.stdout
    ferr = sys.stderr
    generate_script(
        args.pathname, args.script_type, filenames=args.include_file,
        fout=fout, ferr=ferr
    )

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
