fd = open("Combinations.txt", "r")
f = fd.readlines()

def get_num_orderings(text_arr):
    count = 0
    for text in text_arr:
        new_text = text.strip('\n')
        words = new_text.split(",")
        indices = dict()
        for index, word in enumerate(words):
            indices[word] = index
        if indices['leotard'] != 0:
            continue
        if indices['cape'] > indices['hood']:
            continue
        if indices['shorts'] < indices['leotard'] or indices['shorts'] > indices['belt'] or indices['shorts'] > indices['boots']:
            continue
        count += 1

    print(count)

get_num_orderings(f)