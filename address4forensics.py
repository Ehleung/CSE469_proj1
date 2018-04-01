
import argparse

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument( '-L', '--logical',
					help="Calculate the logical address from either the cluster address" +
					 " or the physical address. Either –c or –p must be given."
						)
	parser.parse_args()

main()