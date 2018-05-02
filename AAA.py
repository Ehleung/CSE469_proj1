'''
Brandon Nydam 1208178552
Ellery Leung 1207157168
CSE469 Project 1
'''
import hashlib
import sys

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
    
    partition_start_addrs = []
    FAT_types = []
    #Parsing MBR
    while True:
        testEnd = file.read(2)
        if testEnd.hex().upper() == '55AA':
            break
        file.read(2)     # Skip bytes 0-3
        byte = file.read(1).hex().upper()  # Byte 4, Type of Partition

        file.read(3)     # Skip bytes 5-7


        part_start = ""
        for i in range(4):
            part_start = file.read(1).hex() + part_start
        
        if byte in ('01', '04', '06', '0B', '0C', '1B', '86'):      #Check if FAT type FS  
            partition_start_addrs.append(part_start)
            FAT_types.append(byte)
            
        part_size = ""
        for i in range(4):
            part_size = file.read(1).hex() + part_size
        
        mbr_output = '(' + byte + ') ' + partitionTypes[byte] + ', ' + str(getInt(part_start, 20)).zfill(10)+ ', ' + str(getInt(part_size, 20)).zfill(10)

        print(mbr_output)
    print("\n\n")
    #Parsing VBR    
    #print (partition_start_addrs)
    
    offset = 0 #Need to include offset as each partition does not take into account where file reader is
    for i in range(len(partition_start_addrs)):
        skip_bytes = (getInt(partition_start_addrs[i], 20) - 1) * 512 - offset
        #print ("SKIPPING BYTES: " + str(skip_bytes))
        file.read(skip_bytes)
        offset += skip_bytes
        print("Partition ", i, ": ", partitionTypes[FAT_types[i]])
        #Sectors Per Cluster
        file.read(13)
        byte = file.read(1)
        sectors_per_cluster = getInt(byte.hex(), 20)

        #Reserved Area
        byte = file.read(1).hex()
        byte = file.read(1).hex() + byte

        reserved_sectors = getInt(byte, 20)
        
        num_FAT = getInt(file.read(1).hex(), 20)
        
        byte = ''
        #FAT Area
        if FAT_types[i] in ('01','04','06','86'): #Checking if not 32-bit
            file.read(5)
            byte = file.read(1).hex()
            byte = file.read(1).hex() + byte
            file.read(16)
        else:
            file.read(19)
            for j in range(4):
                byte = file.read(1).hex() + byte
                
        #print (byte)
        size_FAT = getInt(byte, 20)
        total_FAT_sectors= num_FAT * size_FAT
        
        offset += 40 #skipping the amount of bytes that have been read in
        
        #Cluster 2 of FAT: Including start of partition in calculation
        first_cluster = getInt(partition_start_addrs[i], 20) +reserved_sectors + total_FAT_sectors
        
        vbr_output =    "Reserved Area: Start Sector: 0 Ending Sector: " + str(reserved_sectors-1) + " Size: " + str(reserved_sectors) + " Sectors" + \
                        "\nSectors Per Cluster: " + str(sectors_per_cluster) + " Sectors" + \
                        "\nFAT Area: Start Sector " + str(reserved_sectors) + " Ending Sector: " + str(total_FAT_sectors) + \
                        "\nNumber of FATS: " + str(num_FAT) + \
                        "\nSize of Each FAT: " + str(size_FAT) + " Sectors" + \
                        "\nFirst Sector of Cluster Two: Sector " + str(first_cluster) + "\n\n"
                        
        
        print(vbr_output)

        #Starting/Ending Sector
        #Size
        #Sectors Per Cluster
        #FAT Area
        #Number of FATS
        #Size of Each FAT in sectors
        #First Sector of Cluster 2
        
    
    # print('exiting')