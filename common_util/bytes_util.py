# file: bytes_util.py

'''
Utilities for Handling Array of Bytes
'''

import binascii
import sys

class BytesUtility:
    '''
    Implements opearations on array of bytes, extractions from array of bytes,
    and conversion of array of bytes to and from other representations.
    '''

    # --- Bytes Operations

    @staticmethod
    def xor(b1: bytes, b2: bytes, trancate=True):
        '''
        Compute the XOR of two arrays of bytes.

        :param b1: Array of bytes 1
        :param b2: Array of bytes 2
        :type b1: bytes
        :type b2: bytes

        :param trancate: If True, XOR of the stream will only be computed until the end
            of the shorter array of bytes. If False, the remaining of the longer array will
            be appended to the result. This is equivalent to XOR the remaining of the longer
            array with an array of bytes containing all zeroes.
        :type trancate: bool, optional

        :return: The XOR of the two arrays of bytes
        :rtype: bytes
        '''
        result = bytes([v1 ^ v2 for v1, v2 in zip(b1, b2)])
        
        if not trancate:
            b1_len = len(b1)
            b2_len = len(b2)
            if b1_len > b2_len:
                result += b1[b2_len:]
            elif b1_len < b2_len:
                result += b2[b1_len:]
            else:
                # b1_len == b2_len, so do nothing
                pass
            
        return result
    
    # --- Bytes Extractions

    @staticmethod
    def has_sufficient_bytes(data: bytes, offset: int, length: int, pos=0):
        '''
        Check if an array of bytes has enough number of bytes in it.

        :param data: the array of bytes to check
        :type data: bytes

        :param offset: the offset of the first required byte, counting from pos
        :param length: the number of bytes required
        :param pos: the starting position in the array of bytes to check
        :type offset: int
        :type length: int
        :type pos: int, optional

        :return: True if the array of bytes has enough bytes, otherwise False
        :rtype: bool
        '''
        data_length = len(data)
        result = False
        if data_length >= pos + offset + length:
            result = True
        return result

    @staticmethod
    def extract_bytes(data: bytes, offset: int, length: int, pos=0):
        # TODO: change the description 'byte stream' to 'an array of bytes'
        '''
        Extract the required bytes from the byte stream.

        :param data: the byte stream with the bytes to be extracted
        :type data: bytes

        :param offset: the offset of the first byte to extract, counting from pos
        :param length: the number of bytes to extract
        :param pos: the starting position in the byte stream
        :type offset: int
        :type length: int
        :type pos: int, optional

        :return: the extracted bytes
        :rtype: bytes
        '''
        return data[pos+offset:pos+offset+length]

    @staticmethod
    def extract_integer(data: bytes, offset: int, length: int, pos=0, endian='little'):
        '''
        Extract the required bytes from the byte stream and convert to integer.

        :param data: the byte stream with the bytes to be extracted
        :type data: bytes

        :param offset: the offset of the first byte to extract, counting from pos
        :param length: the number of bytes to extract
        :param pos: the starting position in the byte stream
        :type offset: int
        :type length: int
        :type pos: int, optional

        :param endian: the endian to used for converting the bytes to integer;
            (a) acceptable values are 'little' and 'big'
        :type endian: str

        :return: the integer value of the extracted bytes
        :rtype: int
        '''
        return int.from_bytes(data[pos+offset:pos+offset+length], endian)
    
    @staticmethod
    def extract_bytes_until(data: bytes, offset: int, marker: bytes, step=1,
                            pos=0, max_search_length=-1,
                            include_marker=False, empty_if_not_found=False):
        '''
        Extract the bytes from the byte stream until some specified bytes appear.

        :param data: the byte stream with the bytes to be extracted
        :type data: bytes

        :param offset: the offset of the first byte to extract, counting from pos
        :param marker: the specified bytes to search for
        :param step: the number of bytes to advance when searching for marker;
            default is 1
        :param pos: the starting position in the byte stream; default is 0
        :param max_search_length:
        :type offset: int
        :type marker: bytes
        :type step: int, optional
        :type pos: int, optional
        :type max_search_length: int, optional

        :param include_marker: when True, the return result contains the marker;
            when False, the return result does not contain the marker
        :param empty_if_not_found: when True, return an empty bytes if marker is not found;
            when False, return everything from the specified starting position until
            the end of the bytes stream (data)
        :type include_marker: bool, optional
        :type empty_if_not_found: bool, optional

        :return: the extracted bytes
        :rtype: bytes
        '''
        marker_length = len(marker)
        if marker_length <= 0:
            raise ValueError('marker length cannot be zero')
        
        start_pos = pos + offset
        if max_search_length > 0:
            # search until max_search_length bytes, or the end of data
            end_pos = min(len(data), start_pos + max_search_length)
        else:
            end_pos = len(data)

        curr_pos = start_pos
        found = False
        while curr_pos < end_pos:
            if data[curr_pos:curr_pos+marker_length] == marker:
                found = True
                break
            curr_pos += step

        curr_length = curr_pos - start_pos
        if found and include_marker:
            # add the marker if found
            curr_length += marker_length

        extracted_bytes = data[start_pos:start_pos+curr_length]

        if not found and empty_if_not_found:
            extracted_bytes = b''

        return extracted_bytes

    # --- Bytes Conversions
    
    @staticmethod
    def integer_to_bytes(value: int, length=-1, endian='little', signed=False):
        '''
        Convert an integer to bytes.

        :param value: the integer to convert
        :type value: int

        :param length: the number of bytes to convert to;
            if length is zero or negative, this function compute the required length
        :param endian: the endian of the bytes to output;
            (a) acceptable values are 'little' and 'big'
        :param signed: when True, convert to a signed representation;
            (a) used in Python built-in function int.to_bytes()
        :type length: int, optional
        :type endian: str, optional
        :type signed: bool, optional
        
        :raise: OverflowError (raise by int.to_bytes())

        :return: the bytes representation of the integer
        :rtype: bytes
        '''
        if length <= 0:
            # compute length if not given
            bit_length = value.bit_length()
            length = bit_length // 8
            if bit_length % 8 != 0:
                length += 1
        return value.to_bytes(length, endian, signed=signed)
    
    @staticmethod
    def bytes_to_integer(data: bytes, endian='little', signed=False):
        '''
        Convert bytes to an integer.

        :param bytes: the bytes to convert
        :param endian: the endian of the bytes;
            (a) acceptable values are 'little' and 'big'
        :param signed: when True, the bytes is taken to be a signed integer;
            when False, the bytes is taken to be an unsigned integer
        :type bytes: bytes
        :type endian: str, optional
        :type signed: bool, optional

        :return: the integer value from the byte representation
        :rtype: int
        '''
        return int.from_bytes(data, endian, signed=signed)
    
    @staticmethod
    def hex_string_to_bytes(hexstr, sep=''):
        '''
        Convert a hex string to bytes.

        :param hexstr: the hex string; for example, 'BEEF0012'
        :param sep: the separator between the bytes in the hex string;
            for example '-' in the hex string 'BEEF-0012'
        :type hexstr: str
        :type sep: str, optional

        :return: the bytes as represented by the hex string
        :rtype: bytes
        '''
        if len(sep) <= 0:
            result = bytes.fromhex(hexstr)
        else:
            if type(hexstr) == bytes:
                hexstr = hexstr.decode()
            if type(sep) == bytes:
                sep = sep.decode()
            new_hexstr = ''.join(hexstr.split(sep))
            result = bytes.fromhex(new_hexstr)
        return result
    
    @staticmethod
    def bytes_to_hex_string(data: bytes, sep='', bytes_per_sep=1):
        '''
        Convert bytes to a hex string.

        :param bytes: the bytes to convert
        :param sep: the separator to be inserted between the bytes in the
            hex string; for example '-' in the hex string 'BEEF-0012'
        :param bytes_per_sep: the number of bytes between each separator;
            for example, bytes_per_sep means output will be 'BEEF00-12'
        :type bytes: bytes
        :type sep: str, optional
        :type bytes_per_step: int, optional

        :return: the hex string representation of the given bytes
        :rtype: str
        '''
        if len(sep) <= 0:
            result = data.hex()
        else:
            result = data.hex(sep, bytes_per_sep=bytes_per_sep)
        return result

    @staticmethod
    def bytes_rep_to_bytes(rep: str, verbose=False, ferr=sys.stderr):
        '''
        Convert a bytes rep to bytes.

        :param rep: the hex string; for example, 'abc\\\\x00\\\\x01'
        :type rep: str

        :param verbose: when True, will output some debugging information
        :type verbose: bool, optional
        :param ferr: the file id to output the debugging information to
        :type ferr: file id

        :return: the bytes as represented by the bytes rep
        :rtype: bytes
        '''
        result = b''

        rep = rep[2:-1]
        rep_len = len(rep)
        ptr = 0

        while ptr < rep_len:
            if rep[ptr] != '\\':
                # a normal byte which is the representation itself
                this_byte = rep[ptr].encode()
                result += this_byte
                if verbose:
                    print(rep[ptr], this_byte, file=ferr)
                ptr += 1
            elif rep[ptr+1] == 'x':
                # a representation in the form \xhh, where hh is two hexadecimal digits
                this_byte = binascii.unhexlify(rep[ptr+2:ptr+4])
                result += this_byte
                if verbose:
                    print(rep[ptr:ptr+4], this_byte, file=ferr)
                ptr += 4
            else:
                # a representation such as \r, \n, etc.
                c = rep[ptr+1]
                if c == 'r':
                    this_byte = b'\r'
                elif c == 'n':
                    this_byte = b'\n'
                elif c == 't':
                    this_byte = b'\t'
                elif c == '"':
                    this_byte = b'"'
                elif c == '\'':
                    this_byte = b"'"
                elif c == '\\':
                    this_byte = b'\\'
                else:
                    this_byte = b'***unknown(' + rep[ptr:ptr+2].encode() + b')***'
                result += this_byte
                if verbose:
                    print(rep[ptr:ptr+2], this_byte, file=ferr)
                ptr += 2

        return result
    
    @staticmethod
    def bytes_to_bytes_rep(data: bytes):
        '''
        Convert bytes to a bytes represenation, which is how the bytes
        will be printed.

        :param bytes: the bytes to convert
        :type bytes: bytes

        :return: the bytes representation of the given bytes
        :rtype: str
        '''
        return f'{data}'
    
# --- end of file --- #
