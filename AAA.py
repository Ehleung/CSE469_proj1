import hashlib
import sys

DEBUG = True

def hash_checksum(filename):
    if DEBUG:
        print ('Generating Checksums')
        #print ("sha1-{}.txt".format(filename))
    md5file = open("md5-{}.txt".format(filename), 'w+')
    shafile = open("sha1-{}.txt".format(filename), 'w+')
    
    md5file.write(hashlib.md5(open(filename, 'rb').read()).hexdigest())
    shafile.write(hashlib.sha1(open(filename, 'rb').read()).hexdigest())    
    
    md5file.close()
    shafile.close()
    
    if DEBUG:
        print ('Checksums Generated')

if __name__ == "__main__":
    #print(sys.argv[1])

    try:
        open(sys.argv[1], 'r')
    except OSError:
        print ('Error, File not found')
        exit

    print(sys.argv)
    hash_checksum(sys.argv[1])
    print('exiting')
