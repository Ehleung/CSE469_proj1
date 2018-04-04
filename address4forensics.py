import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-L', '--logical', metavar='', help='Calculate the logical address from either the cluster ' +
											'address or the physical address. Either -c or -p must be given.')
results = parser.parse_args()