import argparse

parser = argparse.ArgumentParser()

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

# [–b offset]
parser.add_argument('-b', '--partition-start', dest='offset', type=int, default=0,
					help='Specifies the physical address (sector number) of the partition\'s beginning. ' +
					'Defaults to 0 for ease with single partition images. The offset will always translate '+
					'into logical address 0.')

# Grouping for [-B [-s bytes]]
parser.add_argument('-B', '--byte-address', action='store_true',
					help='Returns the byte address of the calculated value instead of the sector value.')
parser.add_argument('-s', '--sector-size', dest='bytes', type=int, default=512,
					help='Used to specify the bytes per sector when used with \'-B\'. The default is 512.')

# [-l address]
parser.add_argument('-l', '--logical-known', dest='address',
					help='Specifies the known logical address for calculating physical/cluster address. ' +
					'When used with -L, this will simply return the address given.')
# [-p address]
parser.add_argument('-p', '--physical-known', dest='address',
					help='Specifies the known logical address for calculating logical/cluster address. ' +
					'When used with -P, this will simply return the address given.')

# Grouping for [-c address -k sectors -r sectors -t tables -f sectors]
parser.add_argument('-c', '--cluster-known', dest='address',
					help='Specifies the known cluster address for calculating logical/physical address. ' +
					'When used with -C, this will simply return the address given. Note: -k, -r, -t, and -f ' +
					'must be provided with this option.')
parser.add_argument('-k', '--cluster-size', dest='sectors', type=int,
					help='Specifies the number of sectors per cluster.')
parser.add_argument('-r', '--reserved', dest='sectors', type=int,
					help='Specifies the number of reserved sectors in the partition.')
parser.add_argument('-t', '--fat-tables', dest='tables', type=int, default=2,
					help='Specifies the number of FAT tables. The default is 2.')
parser.add_argument('-f', '--fat-length', dest='sectors', type=int,
					help='Specifies the length of each FAT table in sectors.')

args = parser.parse_args()

def test_values():
	print(args.logical)
