'''
Brandon Nydam 1208178552
Ellery Leung 1207157168
CSE469 Project 1
'''
import argparse
import sys

parser = argparse.ArgumentParser(prog='address4forensics')

# Group that takes input for -L|-P|-C
calc_group = parser.add_mutually_exclusive_group(required=True)
calc_group.add_argument('-L', '--logical', action='store_true',
					help='Calculates the logical address from either the cluster ' +
					'address or the physical address. Either -c or -p must be given.')
calc_group.add_argument('-P', '--physical', action='store_true',
					help='Calculates the physical address from either the cluster ' +
					'address or the logical address. Either -c or -l must be given.')
calc_group.add_argument('-C', '--cluster', action='store_true',
					help='Calculates the cluster address from either the logical ' +
					'address or the physical address. Either -l or -p must be given.')

# -b offset
parser.add_argument('-b', '--partition-start', dest='offset', metavar='offset', type=int, default=0,
					help='Specifies the physical address (sector number) of the partition\'s beginning. ' +
					'Defaults to 0 for ease with single partition images. The offset will always translate '+
					'into logical address 0.')

# Grouping for [-B [-s bytes]]
parser.add_argument('-B', '--byte-address', action='store_true', dest='useByte',
					help='Returns the byte address of the calculated value instead of the sector value.')
parser.add_argument('-s', '--sector-size', dest='bytes', metavar='bytes', type=int, default=512,
					help='Used to specify the bytes per sector when used with \'-B\'. The default is 512.')

# [-l address]
parser.add_argument('-l', '--logical-known', metavar='address', dest='logical_address', type=int,
					help='Specifies the known logical address for calculating physical/cluster address. ' +
					'When used with -L, this will simply return the address given.')
# [-p address]
parser.add_argument('-p', '--physical-known', metavar='address', dest='physical_address', type=int,
					help='Specifies the known logical address for calculating logical/cluster address. ' +
					'When used with -P, this will simply return the address given.')

# Grouping for [-c address -k sectors -r sectors -t tables -f sectors]
parser.add_argument('-c', '--cluster-known', metavar='address', dest='cluster_address', type=int,
					help='Specifies the known cluster address for calculating logical/physical address. ' +
					'When used with -C, this will simply return the address given. Note: -k, -r, -t, and -f ' +
					'must be provided with this option.')
parser.add_argument('-k', '--cluster-size', metavar='sectors', dest='cluster_size', type=int,
					help='Specifies the number of sectors per cluster.')
parser.add_argument('-r', '--reserved', metavar='sectors', dest='reserved', type=int,
					help='Specifies the number of reserved sectors in the partition.')
parser.add_argument('-t', '--tables', dest='tables', metavar='tables', type=int, default=2,
					help='Specifies the number of FAT tables. The default is 2.')
parser.add_argument('-f', '--fat-length', metavar='sectors', dest='fat_length', type=int,
					help='Specifies the length of each FAT table in sectors.')

args = parser.parse_args()

#temporary value assignment
returnValue = None

# If logical, need to subtract the offset from address
if args.logical:
	if args.logical_address:
		returnValue = args.logical_address
	elif args.physical_address:
		returnValue = args.physical_address - args.offset
	elif args.cluster_address:
		# Check for valid input in -c parameters
		if args.cluster_size == None or args.reserved == None or args.tables == None or args.fat_length == None:
			print('-k -r -t -f are all required parameters for -c. Please check your input.')
			sys.exit(1)
		else:
			# value = (cluster_known - 2) * sectors per cluster + reserved sectors + (number of tables * number of sectors per table)
			# Don't need to add offset because of logical addr
			temp = ((args.cluster_address - 2) * args.cluster_size) + args.reserved + (args.tables * args.fat_length)

# If physical, need to add the offset to address
elif args.physical:
	if args.physical_address:
		returnValue = args.physical_address
	elif args.logical_address:
		returnValue = args.logical_address + args.offset
	elif args.cluster_address:
		# Check for valid input in -c parameters
		if args.cluster_size == None or args.reserved == None or args.tables == None or args.fat_length == None:
			print('-k -r -t -f are all required parameters for -c. Please check your input.')
			sys.exit(1)
		else:
			# value = offset + (cluster_known - 2) * sectors per cluster + reserved sectors + (number of tables * number of sectors per table)
			returnValue = args.offset + ((args.cluster_address - 2) * args.cluster_size) + args.reserved + (args.tables * args.fat_length)

elif args.cluster:
	if args.cluster_address:
		returnValue = args.cluster_address
	elif args.logical_address:
		returnValue = args.logical_address + args.offset
	elif args.physical_address:
		returnValue = args.physical_address - args.offset

if args.useByte:
	returnValue = returnValue*args.bytes

print (returnValue)
