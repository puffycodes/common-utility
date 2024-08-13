# file: hexdump.py

import string

class HexDump:

    printable = string.ascii_letters + string.digits + string.punctuation + ' '

    @staticmethod
    def hexdump(data, offset=0, length=-1, pos=0, sep=' ', bytes_per_line=16):
        hex_array = HexDump.to_hex_array(data, offset=offset, length=length, pos=pos)
        text_str = HexDump.to_text(data, offset=offset, length=length, pos=pos)
        
        byte_count = len(hex_array)
        hexdump_array = []
        for i in range(0, byte_count, bytes_per_line):
            curr_hex_array = hex_array[i:i+bytes_per_line]
            curr_text_str = text_str[i:i+bytes_per_line]

            curr_byte_count = len(curr_hex_array)
            if curr_byte_count < bytes_per_line:
                padding_count = bytes_per_line - curr_byte_count
                curr_hex_array.extend(['  '] * padding_count)
                curr_text_str += ' ' * padding_count
            curr_hex_str = sep.join(curr_hex_array)

            hexdump_array.append(f'{i:08x}: {curr_hex_str}  |{curr_text_str}|')

        return hexdump_array

    @staticmethod
    def to_hex(data, offset=0, length=-1, pos=0, sep=' '):
        hex_array = HexDump.to_hex_array(data, offset=offset, length=length, pos=pos)
        return sep.join(hex_array)

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
