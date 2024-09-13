# file: bytes_util.py

import binascii
import sys

class BytesUtility:

    # --- Bytes Operations

    @staticmethod
    def xor(b1: bytes, b2: bytes, trancate=True):
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
        data_length = len(data)
        result = False
        if data_length >= pos + offset + length:
            result = True
        return result

    @staticmethod
    def extract_bytes(data: bytes, offset: int, length: int, pos=0):
        return data[pos+offset:pos+offset+length]

    @staticmethod
    def extract_integer(data: bytes, offset: int, length: int, pos=0, endian='little'):
        return int.from_bytes(data[pos+offset:pos+offset+length], endian)
    
    @staticmethod
    def extract_bytes_until(data: bytes, offset: int, marker: bytes, step=1,
                            pos=0, max_search_length=-1,
                            include_marker=False, empty_if_not_found=False):
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
        if include_marker:
            curr_length += marker_length

        extracted_bytes = data[start_pos:start_pos+curr_length]

        if not found and empty_if_not_found:
            extracted_bytes = b''

        return extracted_bytes

    # --- Bytes Conversions
    
    @staticmethod
    def integer_to_bytes(value: int, length=-1, endian='little', signed=False):
        if length <= 0:
            # compute length if not given
            bit_length = value.bit_length()
            length = bit_length // 8
            if bit_length % 8 != 0:
                length += 1
        return value.to_bytes(length, endian, signed=signed)
    
    @staticmethod
    def bytes_to_integer(data: bytes, endian='little', signed=False):
        return int.from_bytes(data, endian, signed=signed)
    
    @staticmethod
    def hex_string_to_bytes(hexstr, sep=''):
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
        if len(sep) <= 0:
            result = data.hex()
        else:
            result = data.hex(sep, bytes_per_sep=bytes_per_sep)
        return result

    @staticmethod
    def bytes_rep_to_bytes(rep: str, verbose=False, ferr=sys.stderr):
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
        return f'{data}'
    
# --- end of file --- #
