fd = open("dataset_317286_6.txt", "r")
inputs = fd.readlines()
f = inputs[1]
n = inputs[0]

adjacency_list = dict()
def get_adjacency_list(text, k):
    global adjacency_list
    size = len(text) - k + 1
    i = 0
    last_komer = ""
    while i < size:
        komer = text[i:i+k]
        # If we haven't seen this komer yet, add a branch for it in adjacency list
        if adjacency_list.get(komer, "DNE") == "DNE":
            # We don't add it if it's the last komer in the string
            if i + k != len(text):
                adjacency_list[komer] = []
        # If the last_komer is a komer (not empty string i.e. current komer is not first komer of string) we append to branch
        if last_komer != "":
            adjacency_list[last_komer].append(komer)
        # Store last komer we saw so we can append next komer to it in its adjacency list
        last_komer = komer
        i += 1

branch_strings = []
def get_branches():
    global adjacency_list
    global branch_strings
    for k, v in adjacency_list.items():
        branch_str = k + " -> "
        for leaf in sorted(v):
            branch_str += leaf + ","
        branch_str = branch_str[0:-1]
        branch_strings.append(branch_str)
    branch_strings = sorted(branch_strings)

get_adjacency_list(f.strip('\n'), int(n)-1)
get_branches()
with open('output.txt', 'w') as filehandle:
    for listitem in branch_strings:
        filehandle.write('%s\n' % listitem)