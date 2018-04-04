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

parser.add_argument('-b', '--partition-start', dest='offset', type=int, default=0,
					help='Specifies the physical address (sector number) of the partition\'s beginning. ' +
					'Defaults to 0 for ease with single partition images. The offset will always translate '+
					'into logical address 0')

parser.add_argument('-l', '--logical-known', dest='address',
					help='Specifies the known logical address for calculating physical/cluster address. ' +
					'When used with -L, this will simply return the address given.')
parser.add_argument('-p', '--physical-known', dest='address',
					help='Specifies the known logical address for calculating logical/cluster address. ' +
					'When used with -P, this will simply return the address given.')
parser.add_argument('-c', '--cluster-known', dest='address',
					help='Specifies the known cluster address for calculating logical/physical address. ' +
					'When used with -C, this will simply return the address given. Note: -k, -r, -t, and -f ' +
					'must be provided with this option.')


args = parser.parse_args()

def test_values():
	print(args.logical)
