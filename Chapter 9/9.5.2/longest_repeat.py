fd = open("dataset_317408_5.txt", "r")
f = fd.readline()

def longest_repeat(text):
    substr_length = len(text) - 1
    end_substr = -1
    while substr_length > 0:
        longest = dict()
        
        chars_to_end = len(text) - substr_length + 1
        shift_window = 1
        start = 0
        end = end_substr
        
        while shift_window <= chars_to_end:
            if end == 0:
                if longest.get(text[start:], "DNE") == "DNE": 
                    longest[text[start:]] = "EXISTS"
                    start += 1
                    end += 1
                else:
                    with open('output.txt', 'w') as filehandle:
                        filehandle.write('%s' % text[start:])
                    return
            else:
                if longest.get(text[start:end], "DNE") == "DNE": 
                    longest[text[start:end]] = "EXISTS"
                    start += 1
                    end += 1
                else:
                    with open('output.txt', 'w') as filehandle:
                        filehandle.write('%s' % text[start:end])
                    return
            shift_window += 1
            
        end_substr -= 1
        substr_length -= 1
            

longest_repeat(f.strip('\n'))