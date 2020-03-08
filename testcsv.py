data = ['12/16/1997 12:19',150,'G',0,'G',112502,'G',4.795,'G',15,'G']
col = int((len(data[1:])))
start = 1
end = 3
returndata = []
for section in range(3):
    returndata.append([data[0]] + data[start:end])
    (start,end) = (end,end+2)
print(returndata)