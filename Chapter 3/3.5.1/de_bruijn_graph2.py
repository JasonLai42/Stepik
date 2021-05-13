fd = open("dataset_317287_8.txt", "r")
f = fd.readlines()

adjacency_list = dict()
def get_adjacency_list(text_arr):
    global adjacency_list
    # -2 to account for the newline
    size = len(text_arr[0]) - 2
    for text in text_arr:
        text = text.strip('\n')
        komer_branch = text[0:size]
        komer_leaf = text[1:]
        # If we haven't seen this komer yet, add a branch for it in adjacency list
        if adjacency_list.get(komer_branch, "DNE") == "DNE":
            # We don't add it if it's the last komer in the string
            adjacency_list[komer_branch] = []
        adjacency_list[komer_branch].append(komer_leaf)

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

get_adjacency_list(f)
get_branches()
with open('output.txt', 'w') as filehandle:
    for listitem in branch_strings:
        filehandle.write('%s\n' % listitem)