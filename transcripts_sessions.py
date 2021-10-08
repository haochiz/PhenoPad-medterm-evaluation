# python3.5+
import re

def load(fn, path):
    ''' Loads the evualtion results 
    '''
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    f = open(path + fn, 'r')
    txt = f.read()
    txt = ansi_escape.sub('', txt)    

    return txt.split('\n')

def truncate_space(line):
    new_line = line[0]
    for char_i in range(1,len(line)-1):
        if not line[char_i].isspace(): new_line += line[char_i]
        else:
            if (not line[char_i-1].isspace()): #or not(line[char_i+1].isspace()):
                new_line += line[char_i]
    new_line += line[-1]
    
    return new_line    

def get_sent_pairs(pair):
    sent_pairs = []
    sent_pairs.append([pair[0].lower(), pair[1].lower()])

    return sent_pairs
    
if __name__ == '__main__':
    lines = load('test_file.txt', './')
    for li, line in enumerate(lines):
        if 'REF: ' in line[:5]:
            print(truncate_space(line).lower())
            print(truncate_space(lines[li+1]).lower())

