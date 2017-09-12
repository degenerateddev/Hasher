import sys
import os
import hashlib
from time import sleep
import optparse
from Crypto.Cipher import AES
import struct
import random


def stringsha256(encstring):
   	key = hashlib.sha256(encstring).digest()
   	sleep(1)
  	print "\n"
   	print key
        print "\n"

def stringsha256(decstring):
	key = hashlib.sha256(decstring).digest() 		# Reverse function 1
	sleep(1)
	print "\n"
	print key
	print "\n"


#-------------------------------------------------#


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

#------------------------------------------------#

def decrypt_file(key, in_filename2, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename2)[0]

    with open(in_filename2, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def main():
	parser = optparse.OptionParser("Usage requires:\n"
							"[--key <encryption and decryption key have to be 32 bit (If blank, it will use the default key)]\n"
							"[--encrypt-string or --encrypt-file]\n"
							"[--decrypt-string or --decrypt-file]\n")
        parser.add_option("--encrypt-string", dest="encstring", type="string", help="specify the string to encrypt")
        parser.add_option("--encrypt-file", dest="encfile", type="string", help="specify the encryption file")
	parser.add_option("--decrypt-string", dest="decstring", type="string", help="specify the string to decrypt")
        parser.add_option("--decrypt-file", dest="decfile", type="string", help="specify the decryption file")
	parser.add_option("--key", dest="key", type="string", help="specify the key to en- and decrypt the file or the string (32 bit)")
        (options, args) = parser.parse_args()
        encstring = options.encstring
        encfile = options.encfile
	decstring = options.decstring
	decfile = options.decfile
	in_filename2 = decfile
	in_filename = encfile
	key = options.key
        """if options.encstring == None:
            if options.encfile == None:
                if options.decstring == None:
                    if options.decfile == None:
                        print parser.usage"""
	if options.key == None:
        	key = "2njvu87rtz74hzg8zghe8gz4t7gzw54z"       # Soon random

	if options.encfile != None and options.decfile == None and options.encstring == None and options.decstring == None:
		encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024)
	elif options.encstring != None and options.decstring == None and options.encfile == None and options.decfile == None:
                stringsha256(encstring)
	elif options.decstring != None and options.encstring == None and options.decfile == None and options.encfile == None:
		stringsha256(decstring)
	elif options.decfile != None and options.encfile == None and options.decstring == None and options.encstring == None:
		decrypt_file(key, in_filename2, out_filename=None, chunksize=64*1024)
        else:
            print parser.usage

	
	

if __name__ == "__main__":
    main()
	
