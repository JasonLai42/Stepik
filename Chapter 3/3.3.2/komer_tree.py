fd = open("dataset_317285_10.txt", "r")
f = fd.readlines()

ends = dict()
branches = dict()

branch_strings = []

def construct_dict(arr):
    global ends
    for element in arr:
        text = element.strip('\n')
        ends[text[1:]] = text

def get_branches(arr):
    global ends
    global branches
    global branch_strings
    for element in arr:
        text = element.strip('\n')
        if ends.get(text[0:-1], "DNE") == "DNE": 
            continue
        else:
            if branches.get(ends[text[0:-1]], "DNE") == "DNE":
                branches[ends[text[0:-1]]] = []
                branches[ends[text[0:-1]]].append(text)
            else:
                branches[ends[text[0:-1]]].append(text)
    for k, v in branches.items():
        branch_str = k + " -> "
        for leaf in v:
            branch_str += leaf + ","
        branch_str = branch_str[0:-1]
        branch_strings.append(branch_str)

construct_dict(f)
get_branches(f)
with open('output.txt', 'w') as filehandle:
    for listitem in branch_strings:
        filehandle.write('%s\n' % listitem)