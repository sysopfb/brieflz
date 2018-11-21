from ctypes import *
import binascii
from collections import namedtuple
import zlib
import struct

brieflz = cdll.LoadLibrary('./blzpack_lib.so')

hdr = namedtuple("Header", "magic level packedsize crc depackedsize")

DEFAULT_BLOCK_SIZE = 1024 * 1024
#MAX_BLOCK_SIZE = (0xFFFFFFFFUL - 0xFFFFFFFFUL / 9UL - 64UL)

def compress_data(data, blocksize, level):
	compressed_data = ""
	while len(data) > 0:
		buf = create_string_buffer(data[:blocksize])
		cb = c_int(len(buf))
		cbOut = brieflz.blz_max_packed_size(blocksize)
		packed = create_string_buffer(cbOut)
		workmem = create_string_buffer(brieflz.blz_workmem_size_level(blocksize,1))
		cbOut = c_int(cbOut)
		retval = brieflz.blz_pack_level(byref(buf), byref(packed), cb, byref(workmem), level)
		if retval > 0:
			temp = packed.raw[:retval]
			tempret = struct.pack(">IIIII", 1651276314, level, len(temp), zlib.crc32(temp) % (1<<32), len(buf)) + temp
			compressed_data += tempret
		else:
			print("Compression Error")
			return None
		data = data[blocksize:]
	return compressed_data
		
def decompress_data(data, blocksize, level):
	decompressed_data = ""
	max_packed_size = brieflz.blz_max_packed_size(blocksize);
	
	(magic,level,packedsize,crc,hdr_depackedsize) = struct.unpack_from('>IIIII', data)
	data = data[20:]
	while magic == 0x626C7A1A and len(data) > 0:
		compressed_data = create_string_buffer(data[:packedsize])
		workdata = create_string_buffer(blocksize)
		depackedsize = brieflz.blz_depack(byref(compressed_data), byref(workdata), c_int(hdr_depackedsize))
		if depackedsize != hdr_depackedsize:
			print("Decompression error")
			return None
		decompressed_data += workdata.raw[:depackedsize]
		data = data[packedsize:]
		if len(data) > 0:
			(magic,level,packedsize,crc,hdr_depackedsize) = struct.unpack_from('>IIIII', data)
			data = data[20:]
		else:
			break
	return decompressed_data

def main():
	#blocksize = DEFAULT_BLOCK_SIZE
	blocksize = 100
	level = 1
	data = "This is a test of brieflz compression"*100
	retval = compress_data(data, blocksize, level)
	if retval != None:
		print("Compression SUCCESS!\nCompressed Data: ")
		print(binascii.hexlify(retval))

		retval = decompress_data(retval, blocksize, level)
		if retval != None and retval == data:
			print("Decompress SUCCESS!\nDecompress Data: ")
			print(retval)


main()	