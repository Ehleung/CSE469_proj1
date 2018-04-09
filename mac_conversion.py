import argparse

parser = argparse.ArgumentParser()

# -T|-D [–f filename | -h hex value ]

conv_group = parser.add_mutually_exclusive_group(required=True)
conv_group.add_argument('-T', action='store_true',
						help='Set this flag to perform a time conversion. ' +
						'Either \'-f\' or \'-h\' must be provided.')
conv_group.add_argument('-D', action='store_true',
						help='Set this flag to perform a date conversion. ' +
						'Either \'-f\' or \'-h\' must be provided.')

param_group = parser.add_mutually_exclusive_group(required=True)

parser.add_argument('-f', dest='filename',
					help='Specifies the path to a filename that includes a hex value')