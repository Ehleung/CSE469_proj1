import hashlib
import sys
import binascii

DEBUG = False

partitionTypes = { '01' : "DOS 12-bit FAT",
                   '04' : "DOS 16-bit FAT for partitions < 32 MB",
                   '05' : "Extended partition",
                   '06' : "DOS 16-bit FAT for partitions > 32 MB",
                   '07' : "NTFS",
                   '08' : "AIX bootable partition",
                   '09' : "AIX data partition",
                   '0B' : "DOS 32-bit FAT",
                   '0C' : "DOS 32-bit FAT for interrupt 13 support",
                   '17' : "Hidden NTFS partition (XP and earlier)",
                   '1B' : "Hidden FAT32 partition",
                   '1E' : "Hidden VFAT partition",
                   '3C' : "Partition Magic recovery partition",
                   '66' : "Novell partitions",
                   '67' : "Novell partitions",
                   '68' : "Novell partitions",
                   '69' : "Novell partitions",
                   '81' : "Linux",
                   '82' : "Linux swap partition/Solaris Partition",
                   '83' : "Linux native file systems",
                   '86' : "FAT16 volume/stripe set (Windows NT)",
                   '87' : "HPFS or NTFS volume/stripe set",
                   'A5' : "FreeBSD and BSD/386",
                   'A6' : "OpenBSD",
                   'A9' : "NetBSD",
                   'C7' : "Typical of a corrupted NTFS volume/stripe set",
                   'EB' : "BeOS"
                   }

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

def getInt(byte, size):
    sector = bin(int(byte, 16)).split('0b')[1]
    sector = sector.zfill(size)
    return int(sector[0:size],2)

if __name__ == "__main__":
    if DEBUG:
        print(sys.argv)
    file = None
    list = []
    try:
        file = open(sys.argv[1], 'rb')
    except OSError:
        print ('Error, File not found')
        exit

    hash_checksum(sys.argv[1])
    file.read(446)   # Skip executable code
    while True:
        testEnd = file.read(2)
        if testEnd.hex().upper() == '55AA':
            break
        file.read(2)     # Skip bytes 0-3
        byte = file.read(1).hex().upper()  # Byte 4, Type of Partition
        
        file.read(3)     # Skip bytes 5-7

        partition_start_addrs = []

        part_start = ""
        for i in range(4):
            part_start = file.read(1).hex() + part_start
        partition_start_addrs.append(part_start)

        part_size = ""
        for i in range(4):
            part_size = file.read(1).hex() + part_size
        
        mbr_output = '(' + byte + ') ' + partitionTypes[byte] + ', ' + str(getInt(part_start, 20)).zfill(10)+ ', ' + str(getInt(part_size, 20)).zfill(10)

        print(mbr_output)
    # print('exiting')
