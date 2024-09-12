# file: hexdump.py

import sys
import string
import argparse

class HexDump:

    printable = string.ascii_letters + string.digits + string.punctuation + ' '
    default_filler_line = f'--------: .....'
    # default_filler_line = f'          <snipped>'

    @staticmethod
    def hexdump(data, offset=0, length=-1, pos=0,
                sep=' ', bytes_per_line=16, pos_label=-1, align_front=True):
        if pos_label < 0:
            pos_label = pos + offset

        hex_array = []
        text_str = ''

        # Pad at the front to align to bytes_per_line boundary
        if align_front:
            front_padding_count = pos_label % bytes_per_line
            if front_padding_count != 0:
                hex_array = ['  '] * front_padding_count
                text_str = ' ' * front_padding_count
                pos_label = pos_label - (pos_label % bytes_per_line)
        
        # Add the hexdump and text representation
        hex_array.extend(
            HexDump.to_hex_array(data, offset=offset, length=length, pos=pos)
        )
        text_str += HexDump.to_text(data, offset=offset, length=length, pos=pos)

        # Pad at the back to align to bytes_per_line boundary
        byte_count = len(hex_array)
        last_line_byte_count = byte_count % bytes_per_line
        if last_line_byte_count != 0:
            back_padding_count = bytes_per_line - last_line_byte_count
            hex_array.extend(['  '] * back_padding_count)
            text_str += ' ' * back_padding_count
            byte_count += back_padding_count

        # Output the hexdump as array of text
        hexdump_array = []
        for i in range(0, byte_count, bytes_per_line):
            curr_hex_array = hex_array[i:i+bytes_per_line]
            curr_text_str = text_str[i:i+bytes_per_line]
            curr_hex_str = HexDump.hex_array_to_string(curr_hex_array, sep=sep)
            hexdump_array.append(
                f'{(i+pos_label):08x}: {curr_hex_str}  |{curr_text_str}|'
            )

        return hexdump_array
    
    @staticmethod
    def hexdump_start_and_end(data, byte_count_start=48, byte_count_end=48,
                              sep=' ', bytes_per_line=16, pos_label=-1,
                              align_front=True, filler_line=''):
        if byte_count_start < 0:
            byte_count_start = 0
        if byte_count_end < 0:
            byte_count_end = 0

        data_length = len(data)

        hexdump_array = []
        if data_length > byte_count_start + byte_count_end:
            if byte_count_start > 0:
                # hexdump the starting bytes
                hexdump_array.extend(
                    HexDump.hexdump(
                        data, offset=0, length=byte_count_start,
                        sep=sep, bytes_per_line=bytes_per_line, pos_label=pos_label,
                        align_front=align_front
                    )
                )
            # add in the filler line
            if filler_line == '':
                hexdump_array.append(HexDump.default_filler_line)
            else:
                hexdump_array.append(filler_line)
            if byte_count_end > 0:
                # hexdump the ending bytes
                end_offset = data_length - byte_count_end
                if pos_label < 0:
                    end_pos_label = -1
                else:
                    end_pos_label = pos_label + end_offset
                hexdump_array.extend(
                    HexDump.hexdump(
                        data, offset=end_offset, length=byte_count_end,
                        sep=sep, bytes_per_line=bytes_per_line, pos_label=end_pos_label,
                        align_front=align_front
                    )
                )
        else:
            # hexdump the whole data if it is too short
            hexdump_array = HexDump.hexdump(
                data, sep=sep, bytes_per_line=bytes_per_line,
                pos_label=pos_label, align_front=align_front
            )

        return hexdump_array
    
    @staticmethod
    def brief_hexdump(hexdump_array, start_line=0, end_line=0, filler_line=''):
        result = hexdump_array
        if start_line < 0:
            start_line = 0
        if end_line < 0:
            end_line = 0
        if start_line + end_line <= 0:
            return result
        if start_line + end_line < len(hexdump_array):
            result = []
            if start_line > 0:
                result.extend(hexdump_array[:start_line])
            if filler_line == '':
                result.append(HexDump.default_filler_line)
            else:
                result.append(filler_line)
            if end_line > 0:
                result.extend(hexdump_array[-end_line:])
        return result
    
    @staticmethod
    def print_hexdump(hexdump_array, prefix='', fout=sys.stdout):
        for str in hexdump_array:
            print(f'{prefix}{str}', file=fout)
        return
    
    @staticmethod
    def hexdump_and_print(data_list, label_list=[], pos_label_list=[],
                          sep=' ', bytes_per_line=16, max_bytes_show=-1, filler_line='',
                          prefix='', sep_line='', fout=sys.stdout):
        count = 0
        label_list_length = len(label_list)
        pos_label_list_length = len(pos_label_list)
        for curr_data in data_list:
            curr_label = label_list[count] if count < label_list_length else ''
            curr_pos_label = pos_label_list[count] if count < pos_label_list_length else -1
            if max_bytes_show <= 0 or len(curr_data) < max_bytes_show:
                hexdump_array = HexDump.hexdump(
                    curr_data, sep=sep, bytes_per_line=bytes_per_line,
                    pos_label=curr_pos_label
                )
            else:
                bytes_count_start = max_bytes_show // 2
                bytes_count_end = max_bytes_show - bytes_count_start
                hexdump_array = HexDump.hexdump_start_and_end(
                    curr_data, byte_count_start=bytes_count_start, byte_count_end=bytes_count_end,
                    sep=sep, bytes_per_line=bytes_per_line, pos_label=curr_pos_label,
                    filler_line=filler_line
                )
            if curr_label != '':
                print(f'{curr_label}', file=fout)
            HexDump.print_hexdump(hexdump_array, prefix=prefix, fout=fout)
            print(f'{sep_line}', file=fout)
            count += 1
        return

    @staticmethod
    def to_hex(data, offset=0, length=-1, pos=0, sep=' '):
        hex_array = HexDump.to_hex_array(data, offset=offset, length=length, pos=pos)
        return HexDump.hex_array_to_string(hex_array, sep=sep)

    @staticmethod
    def to_hex_array(data, offset=0, length=-1, pos=0):
        start_pos, end_pos = HexDump.pos_from_offset(len(data), offset=offset, length=length, pos=pos)
        hex_array = [f'{c:02X}' for c in data[start_pos:end_pos]]
        return hex_array
    
    @staticmethod
    def to_text(data, offset=0, length=-1, pos=0):
        start_pos, end_pos = HexDump.pos_from_offset(len(data), offset=offset, length=length, pos=pos)
        text_array = [HexDump.char_to_text(c) for c in data[start_pos:end_pos]]
        return ''.join(text_array)
    
    # --- Internal Functions
    
    @staticmethod
    def char_to_text(c, non_printable='.'):
        cc = chr(c)
        return cc if cc in HexDump.printable else non_printable
    
    @staticmethod
    def hex_array_to_string(hex_array, sep=' '):
        sep_length = len(sep)
        if sep == ' ' or sep_length <= 0:
            # - special cases when separator is a space (' ') or empty ('')
            return sep.join(hex_array)
        result = ''
        for i in range(len(hex_array) - 1):
            result += hex_array[i]
            # - insert separator only between two hex strings that are
            #   not empty (i.e. space)
            if hex_array[i] != '  ' and hex_array[i+1] != '  ':
                result += sep
            else:
                result += ' ' * sep_length
        result += hex_array[-1]
        return result
    
    @staticmethod
    def pos_from_offset(data_length, offset=0, length=-1, pos=0):
        start_pos = pos + offset
        if length <= 0:
            end_pos = data_length
        else:
            end_pos = start_pos + length
        if end_pos > data_length:
            end_pos = data_length
        return start_pos, end_pos
    
    # --- Main function

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(
            prog='hexdump',
            description='Show a file in hex format.',
            epilog='"Everyone likes to write their own hexdump."'
        )
        parser.add_argument('filename', nargs='+',
                            help='file to show')
        args = parser.parse_args()

        for file in args.filename:
            print(f'=== file: {file}')
            with open(file, 'rb') as fd:
                data = fd.read()
            hexdump_array = HexDump.hexdump(data)
            HexDump.print_hexdump(hexdump_array)
            print()
        return
    
if __name__ == '__main__':
    HexDump.main()

# --- end of file --- #
