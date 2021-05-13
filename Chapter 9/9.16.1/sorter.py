fd = open("test.txt", "r")
inputs = fd.readlines()
inputs = sorted(inputs)
with open('testout.txt', 'w') as filehandle:
    for listitem in inputs:
        filehandle.write('%s' % listitem)