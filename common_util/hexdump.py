# file: hexdump.py

'''
Output Bytes in Pretty Format

The class HexDump implements a few methods to output bytes in pretty format.
'''

import sys
import string
import argparse

class HexDump:

    # The list of printable characters for the purpose of this class.
    # This list is different from string.printable.
    printable = string.ascii_letters + string.digits + string.punctuation + ' '

    # The default line to fill for the gap in hexdump_start_and_end()
    default_filler_line = f'--------: .....'
    # default_filler_line = f'          <snipped>'

    @staticmethod
    def hexdump(data, offset=0, length=-1, pos=0,
                sep=' ', bytes_per_line=16, pos_label=-1, align_front=True):
        '''
        Output byte stream in pretty format, formatting as hexadecimal and text with
        position as tag.

        :param data: contains the byte stream to output
        :type data: bytes

        :param offset: the offset of the first byte to output, counting from pos
        :type offset: int, optional
        :param length: the number of bytes to output;
            (a) zero or negative value means output till the end of bytes stream
        :type length: int, optional
        :param pos: the starting position of byte stream to output
        :type pos: int, optional

        :param sep: the separator to used between the hexadecimal formatting
        :type sep: bytes, optional
        :param bytes_per_line: the maximum number of bytes to show per line of output
        :type bytes_per_line: int, optional
        :param pos_label: the value of the tag to label the first output byte;
            (a) negative value means the tag will be computed from (pos + offset)
        :type pos_label: int, optional
        :param align_front: align the front bytes to the proper position base on the
            boundary indicated by bytes_per_line
        :type align_front: bool, optional

        :return: An array contains the byte stream in pretty format
        :rtype: list of str
        '''
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
        '''
        Output the start and end bytes of a byte stream in pretty format, formatting
        as hexadecimal and text with position as tag.

        :param data: the byte stream to output
        :type data: bytes

        :param byte_count_start: the maximum number of bytes to output at the start
        :type byte_count_start: int, optional
        :param byte_count_end: the maximum number of bytes to output at the end;
            (a) when the sum of byte_count_start and byte_count_end exceeds the
            entire length of the byte stream, the whole byte strem is output
        :type byte_count_end: int, optional

        :param sep: the separator to used between the hexadecimal forrmatting
        :type sep: bytes, optional
        :param bytes_per_line: the maximum number of bytes to show per line of out
        :type bytes_per_line: int, optional
        :param pos_label: the value of the tag to label the first output byte;
            (a) negative value means the tag will be the position of the byte in data
        :type pos_label: int, optional
        :param align_front: align the front bytes to the proper position base on the
            boundary indicated by bytes_per_line
        :type align_front: bool, optional

        :param filler_line: the line to use to indicate the gap between the start
            bytes and end bytes, if any
        :type filler_line: str, optional

        :return: An array contains the indicated portion of the byte stream in pretty
            format
        :rtype: list of str
        '''
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
        '''
        Extract the start and end portion of the hexdump output from functions
        such as hexdump() and hexdump_start_and_end().

        :param hexdump_array: the output from the hexdump functions
        :type hexdump_array: list of str

        :param start_line: the number of lines to extract at the start of the hexdump
        :type start_line: int, optional
        :param end_line: the number of lines to extract at the end of the hexdump;
            (a) when the sum of start_line and end_line exceeds the total number
            of lines in hexdump_array, the entire hexdump is returned
        :type end_line: int, optional

        :param filler_line: the line to use to indicate the gap between the start
            lines and end lines, if any
        :type filler_line: str, optional

        :return: the abridge copy of the given hexdump
        :rtype: list of str
        '''
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
        '''
        Print the hexdump output from the hexdump functions.

        :param hexdump_array: the output from the hexdump functions
        :type hexdump_array: list of str
        :param prefix: the string to print before every line of hexdump_array
        :type prefix: str, optional
        :param fout: the file id of the output (default is sys.stdout)
        :type fout: file id

        :return: no value is returned by this function
        '''
        for str in hexdump_array:
            print(f'{prefix}{str}', file=fout)
        return
    
    @staticmethod
    def hexdump_and_print(data_list, label_list=[], pos_label_list=[],
                          sep=' ', bytes_per_line=16, max_bytes_show=-1, filler_line='',
                          prefix='', sep_line='', fout=sys.stdout):
        '''
        Print the hexdump of a list of byte stream.

        :param data_list: the list of byte stream
        :type data_list: list of bytes
        :param label_list: the list of label to print before the hexdump of the corresponding
            byte stream
        :type label_list: list of str, optional
        :param pos_label_list: the list of pos_label (to be used when calling hexdump() functions)
            of the corresponding byte stream
        :type pos_label_list: list of int, optional

        :param sep: the sep for calling hexdump() functions
        :type sep: bytes, optional
        :param bytes_per_line: the bytes_per_line for calling hexdump() functions
        :type bytes_per_line: int, optional
        :param max_bytes_show: the maximum number of bytes show in the hexdump;
            (a) about half of max_bytes_show number of bytes will be show at the beginning of
            the hexdump, and the rest at the end of the hexdump
        :type max_bytes_show: int, optional

        :param filler_line: the filler_line for calling hexdump_start_and_end()
        :type filler_line: str, optional

        :param prefix: the prefix for calling print_hexdump()
        :type prefix: str, optional
        :param sep_line: the line to print between each hexdump
        :type sep_line: str, option
        :param fout: the file id of the output (default is sys.stdout)
        :type fout: file id

        :return: no value is returned by this function
        '''
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
        '''
        Convert a byte stream to a sting of hexadecimal representation.

        :param data: the byte stream
        :type data: bytes

        :param offset: the range of bytes to output
            - see hexdump() function
        :type offset: int, optional
        :param length: the range of bytes to output
            - see hexdump() function
        :type length: int, optional
        :param pos: the range of bytes to output
            - see hexdump() function
        :type pos: int, optional

        :param sep: separator to insert between each byte
        :type sep: str, optional

        :return: the string of hexadecimal representation
        :rtype: str
        '''
        hex_array = HexDump.to_hex_array(data, offset=offset, length=length, pos=pos)
        return HexDump.hex_array_to_string(hex_array, sep=sep)

    @staticmethod
    def to_hex_array(data, offset=0, length=-1, pos=0):
        '''
        Convert a byte stream to a list of hexadecimal representation for each of
        the byte.

        :param data: the byte stream
        :type data: bytes

        :param offset: the range of bytes to output
            - see hexdump() function
        :type offset: int, optional
        :param length: the range of bytes to output
            - see hexdump() function
        :type length: int, optional
        :param pos: the range of bytes to output
            - see hexdump() function
        :type pos: int, optional

        :return: a list of the hexadecimal representation of the byte stream
        :rtype: list of str
        '''
        start_pos, end_pos = HexDump.pos_from_offset(len(data), offset=offset, length=length, pos=pos)
        hex_array = [f'{c:02X}' for c in data[start_pos:end_pos]]
        return hex_array
    
    @staticmethod
    def to_text(data, offset=0, length=-1, pos=0):
        '''
        Convert a byte stream to a string of text.

        :param data: the byte stream
        :type data: bytes

        :param offset: the range of bytes to output
            - see hexdump() function
        :type offset: int, optional
        :param length: the range of bytes to output
            - see hexdump() function
        :type length: int, optional
        :param pos: the range of bytes to output
            - see hexdump() function
        :type pos: int, optional

        :return: the string of text representation
        :rtype: str
        '''
        start_pos, end_pos = HexDump.pos_from_offset(len(data), offset=offset, length=length, pos=pos)
        text_array = [HexDump.char_to_text(c) for c in data[start_pos:end_pos]]
        return ''.join(text_array)
    
    # --- Internal Functions
    
    @staticmethod
    def char_to_text(c, non_printable='.'):
        '''
        (Internal) Return the text representation of the given character.

        :param c: the character to convert to text representation
        :type c: int
        :param non_printable: the text representation to be used if the character c
            is not printable
        :type non_printable: str, optional

        :return: the text representation of the given character c
        :rtype: str
        '''
        cc = chr(c)
        return cc if cc in HexDump.printable else non_printable
    
    @staticmethod
    def hex_array_to_string(hex_array, sep=' '):
        '''
        (Internal) Convert a list hexadecimal representation to a single string.

        :param hex_array: the list of hexadecimal
        :type hex_array: list of str
        :param sep: the character(s) to insert between the individual hexadeciaml
            representation;
            (a) sep can be an empty string (i.e. '');
            (b) sep will not be inserted between two elements of the list if any
            of them is empty (i.e. contain only space);
            an equivalent number of spaces will be inserted instead
        :type sep: str, optional

        :return: the list of dexadeciaml representation as a single string
        :rtype: str
        '''
        sep_length = len(sep)
        if sep == ' ' or sep_length <= 0:
            # - special cases when separator is a space (' ') or empty ('')
            return sep.join(hex_array)
        result = ''
        for i in range(len(hex_array) - 1):
            result += hex_array[i]
            # - insert separator only between two hex strings that are
            #   not empty (i.e. space)
            # - otherwise insert the equivalent amount of space instead
            if hex_array[i] != '  ' and hex_array[i+1] != '  ':
                result += sep
            else:
                result += ' ' * sep_length
        result += hex_array[-1]
        return result
    
    @staticmethod
    def pos_from_offset(data_length, offset=0, length=-1, pos=0):
        '''
        (Internal) Calculate the start and end position.

        This function is used by hexdump() to compute the start and end positions.

        :param data_length: the length of the entire byte stream
        :type data_length: int
        :param offset: the offset of the first byte to output, counting from pos
        :type offset: int, optional
        :param length: the number of bytes to output;
            (a) zero or negative value means output till the end of bytes stream
        :type length: int, optional
        :param pos: the starting position of byte stream to output
        :type pos: int, optional

        :return: (start_pos, end_post), where start_pos is the position of the starting byte,
            and end_pos is the position of the ending bytes plus 1
        :rtype: tuple
        '''
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
        '''
        Take a list of filename and print their hexdump on sys.stdout.

        This function is called when this module is run as main.

        usage: python common_util/hexdump.py <filename> ...
        '''
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
