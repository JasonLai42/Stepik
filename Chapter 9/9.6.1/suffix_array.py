fd = open("dataset_317409_2.txt", "r")
f = fd.readline().strip('\n')

suffix_array = []

def construct_array(text):
    for index, character in enumerate(text):
        suffix_array.append((text[index:], index))

construct_array(f[:-1])
suffix_array.append(('', len(f) - 1))
suffix_array = sorted(suffix_array, key=lambda x: x[0])
suffix_array = [(suffix[0] + '$', suffix[1]) for suffix in suffix_array]
with open('output.txt', 'w') as filehandle:
    for listitem in suffix_array:
        filehandle.write('%s, ' % listitem[1])