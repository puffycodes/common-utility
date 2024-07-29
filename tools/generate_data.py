# file: generate_data.py

import argparse
import sys

def get_size_in_bytes(size_str):
    return int(size_str)

def generate_data(size, verbose=False, fout=sys.stdout, ferr=sys.stderr):
    if verbose:
        print(f'generate {size} bytes of data', file=ferr)
    data = 'a' * 1024
    block_count = size // 1024
    remaining_byte = size % 1024
    for i in range(block_count):
        print(data, end='', file=fout)
    for i in range(remaining_byte):
        print('a', end='', file=fout)
    return

def main():
    parser = argparse.ArgumentParser(
        prog='generate_data',
        description='Generate the stated amount of data.'
    )
    parser.add_argument('--size', default='1024',
                        help='amount of data to generate')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='provide more information while running')
    args = parser.parse_args()

    fout = sys.stdout
    ferr = sys.stderr

    size_in_bytes = get_size_in_bytes(args.size)
    generate_data(size_in_bytes, verbose=args.verbose)

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
