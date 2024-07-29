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

def mismatch_warning(script_type, os_name, ferr=sys.stderr):
    print(
        f'Warning: script type ({script_type}) generated on this os ({os_name}) may not work correctly',
        file=ferr
    )
    return

def generate_script(path_list, script_type, fout=sys.stdout, ferr=sys.stderr):
    abs_path_list = []
    for path in path_list:
        abs_path = os.path.abspath(os.path.join(path))
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
    generate_script(args.pathname, args.script_type, fout=fout, ferr=ferr)

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
