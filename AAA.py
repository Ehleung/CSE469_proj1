import hashlib
import sys

DEBUG = True

def hash_checksum(filepath):
    if DEBUG:
        print ('Generating Checksums')
        #print ("sha1-{}.txt".format(filename))

    filename = filepath.split("/")[-1]
    filename = filename.split(".")[-2]
    #print (filename)
    md5file = open("md5-{}.txt".format(filename), 'w+')
    shafile = open("sha1-{}.txt".format(filename), 'w+')
    
    md5file.write(hashlib.md5(open(filepath, 'rb').read()).hexdigest())
    shafile.write(hashlib.sha1(open(filepath, 'rb').read()).hexdigest())    
    
    md5file.close()
    shafile.close()
    
    if DEBUG:
        print ('Checksums Generated')


if __name__ == "__main__":
    if DEBUG:
        print(sys.argv)

    try:
        open(sys.argv[1], 'r')
    except OSError:
        print ('Error, File not found')
        exit

    hash_checksum(sys.argv[1])
print('exiting')
