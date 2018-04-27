import argparse

DEBUG = True

parser = argparse.ArgumentParser(add_help = False)

conv_group = parser.add_mutually_exclusive_group(required = True)
conv_group.add_argument('-T', action='store_true')
conv_group.add_argument('-D', action='store_true')

param_group = parser.add_mutually_exclusive_group(required = True)
param_group.add_argument('-f', dest='filename')
param_group.add_argument('-h', dest='hexval')

args = parser.parse_args()

if DEBUG:
	print (args)

print('D')
dates = { 1 : 'Jan',
          2 : 'Feb',
          3 : 'Mar',
          4 : 'Apr',
          5 : 'May',
          6 : 'June',
          7 : 'July',
          8 : 'Aug',
          9 : 'Sep',
          10: 'Oct',
          11: 'Nov',
          12: 'Dec'}

def getHex():
    if args.filename:
        if DEBUG:
            print('Reading data from File')
	file = open(args.filename, 'r')
        var = ""
        while not var:
	    var = file.readline()
            var = var.split("0x", 1)
            if len(var) == 1:
                var = ""
            print(var)
	
        var = var[-1][0:4]
        print(var)
	file.close()
    else:
        var = args.hexval
    return var    


if __name__ == "__main__":
    hexVal = getHex()
    binVal = bin(int(hexVal, 16)).split('0b')[1]
    binVal = binVal.zfill(16)
    print(binVal)

    if args.T: #parse for time
        time = "Time: "
        TD = 'AM'
        if DEBUG:
            print(binVal[0:5],2)
            print(binVal[5:11],2)
            print(binVal[11:16],2)
        hour = int(binVal[0:5],2)
        if hour > 12:
            hour = hour - 12
            TD = 'PM'
        time += str(hour) + ':' + str(int(binVal[5:11],2)) + ":" + str(2*int(binVal[11:16],2)).zfill(2) + " " + TD
        print(time) 
    else:  #parse for date
        date = "Date: "

        if DEBUG:
            print(int(binVal[0:7],2))
            print(dates[int(binVal[7:11],2)])
            print(int(binVal[11:15],2))

        date += dates[int(binVal[7:11],2)] + " " + str(int(binVal[11:16],2)) + ", " +str(int(binVal[0:7],2) + 1980)
        print(date)
