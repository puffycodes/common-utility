# file: hexdump.py

import string
from turtle import back

from numpy import bytes_

class HexDump:

    printable = string.ascii_letters + string.digits + string.punctuation + ' '

    @staticmethod
    def hexdump(data, offset=0, length=-1, pos=0,
                sep=' ', bytes_per_line=16, pos_label=-1):
        if pos_label < 0:
            pos_label = pos + offset

        # Pad at the front to align to bytes_per_line boundary
        front_padding_count = pos_label % bytes_per_line
        if front_padding_count != 0:
            hex_array = ['  '] * front_padding_count
            text_str = ' ' * front_padding_count
            pos_label = pos_label - (pos_label % bytes_per_line)
        else:
            hex_array = []
            text_str = ''
        
        # Add the hexdump
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
            hexdump_array.append(f'{(i+pos_label):08x}: {curr_hex_str}  |{curr_text_str}|')

        return hexdump_array

    @staticmethod
    def to_hex(data, offset=0, length=-1, pos=0, sep=' '):
        hex_array = HexDump.to_hex_array(data, offset=offset, length=length, pos=pos)
        return HexDump.hex_array_to_string(hex_array, sep=sep)

    @staticmethod
    def to_hex_array(data, offset=0, length=-1, pos=0):
        start_pos, end_pos = HexDump.compute_pos(len(data), offset=offset, length=length, pos=pos)
        hex_array = [f'{c:02X}' for c in data[start_pos:end_pos]]
        return hex_array
    
    @staticmethod
    def to_text(data, offset=0, length=-1, pos=0):
        start_pos, end_pos = HexDump.compute_pos(len(data), offset=offset, length=length, pos=pos)
        text_array = [HexDump.char_to_text(c) for c in data[start_pos:end_pos]]
        return ''.join(text_array)
    
    @staticmethod
    def char_to_text(c, non_printable='.'):
        cc = chr(c)
        return cc if cc in HexDump.printable else non_printable
    
    @staticmethod
    def hex_array_to_string(hex_array, sep=' '):
        sep_length = len(sep)
        if sep == ' ' or sep_length <= 0:
            return sep.join(hex_array)
        result = ''
        for i in range(len(hex_array) - 1):
            result += hex_array[i]
            if hex_array[i] != '  ' and hex_array[i+1] != '  ':
                result += sep
            else:
                result += ' ' * sep_length
        result += hex_array[-1]
        return result
    
    @staticmethod
    def compute_pos(data_length, offset=0, length=-1, pos=0):
        start_pos = pos + offset
        if length <= 0:
            end_pos = data_length
        else:
            end_pos = start_pos + length
        if end_pos > data_length:
            end_pos = data_length
        return start_pos, end_pos

# --- end of file --- #
