fd = open("dataset_317284_3.txt", "r")
inputs = fd.readlines()
f = inputs[1]
n = inputs[0]

komer_array = []
    
def get_komers(text, k):
    global komer_array
    size = len(text) - k + 1
    i = 0
    while i < size:
        komer_array.append(text[i:i+k])
        i += 1

get_komers(f.strip('\n'), int(n))
with open('output.txt', 'w') as filehandle:
    for listitem in komer_array:
        filehandle.write('%s\n' % listitem)