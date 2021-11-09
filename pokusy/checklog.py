

searchstr = "Exit Message:"
searchstr1 = "OK"

fopen = open("C:\\Temp\work\\TLRS-channels\\testlog.log", mode = "r")
fread = fopen.readlines()
for line in fread:
    if searchstr in line:
        if not searchstr1 in line:
            print(line)