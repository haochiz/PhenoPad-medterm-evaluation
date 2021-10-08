# python3.5+

def load(fn, path):
    ''' Loads the evualtion results 
    '''
    f = open(path + fn, 'r')
    lines = f.read().split('\n')
    
    return lines

def truncate_space(line):
    new_line = line[0]
    for char_i in range(1,len(line)-1):
        if not line[char_i].isspace(): new_line += line[char_i]
        else:
            if (not line[char_i-1].isspace()): #or not(line[char_i+1].isspace()):
                new_line += line[char_i]
    new_line += line[-1]
    
    return new_line    

def get_sent_pairs(lines):
    sent_pairs = []
    for li, line in enumerate(lines):
        if 'REF: ' in line[:5]:
            sent_pairs.append([truncate_space(line).lower(), truncate_space(lines[li+1]).lower()])

    return sent_pairs
    
if __name__ == '__main__':
    lines = load('test_file.txt', './')
    for li, line in enumerate(lines):
        if 'REF: ' in line[:5]:
            print(truncate_space(line).lower())
            print(truncate_space(lines[li+1]).lower())

