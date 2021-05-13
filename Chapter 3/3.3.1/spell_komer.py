fd = open("dataset_317285_3.txt", "r")
inputs = fd.readlines()
first = inputs[0]
f = inputs[1:]

final_str = ""
    
def spell_komer(first, arr):
    global final_str
    final_str += first.strip('\n')
    index = len(first.strip('\n')) - 1
    for text in arr:
        final_str += text.strip('\n')[index]

spell_komer(first, f)
with open('output.txt', 'w') as filehandle:
        filehandle.write('%s\n' % final_str)