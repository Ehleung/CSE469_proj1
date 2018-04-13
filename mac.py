import argparse

DEBUG = True

parser = argparse.ArgumentParser(add_help = False)

conv_group = parser.add_mutually_exclusive_group(required = True)
conv_group.add_argument('-T', action='store_true',
						help='Set this flag to perform a time conversion. ' +
						'Either \'-f\' or \'-h\' must be provided.')
conv_group.add_argument('-D', action='store_true',
						help='Set this flag to perform a date conversion. ' +
						'Either \'-f\' or \'-h\' must be provided.')

param_group = parser.add_mutually_exclusive_group(required = True)


param_group.add_argument('-f', dest='filename', help='Specifies the path to a filename that includes a hex value')
param_group.add_argument('-h', dest='hexval', help='Specifies the Hex value to convert')

args = parser.parse_args()
if DEBUG:
	print (args)


if args.T:
	print('T')
	file = open(args.filename, 'r')
	var = file.readline()
	file.close()
else:
    var = args.hexval
    
    
    print('D')