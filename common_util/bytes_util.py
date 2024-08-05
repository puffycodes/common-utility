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
    def has_sufficient_bytes(data, offset, length, pos=0):
        data_length = len(data)
        result = False
        if data_length >= pos + offset + length:
            result = True
        return result

    @staticmethod
    def extract_bytes(data, offset, length, pos=0):
        return data[pos+offset:pos+offset+length]

    @staticmethod
    def extract_integer(data, offset, length, pos=0, endian='little'):
        return int.from_bytes(data[pos+offset:pos+offset+length], endian)

    # --- Bytes Conversions
    
    @staticmethod
    def integer_to_bytes(value, length, endian='little', signed=False):
        return value.to_bytes(length, endian, signed=signed)
    
    @staticmethod
    def bytes_to_integer(data, endian='little', signed=False):
        return int.from_bytes(data, endian, signed=signed)
    
    @staticmethod
    def hex_string_to_bytes(hexstr):
        return binascii.unhexlify(hexstr)
    
    @staticmethod
    def bytes_to_hex_string(data, sep='', bytes_per_sep=1):
        return binascii.hexlify(data, sep=sep, bytes_per_sep=bytes_per_sep)

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
    
# --- end of file --- #