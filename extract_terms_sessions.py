# python3.5+
import subprocess
import json
import re

def find_matches(sentence):
    content = '{\"text\":\"%s\"}' % (sentence)
    uri = 'https://ncr.ccm.sickkids.ca/curr/annotate/'

    command_list = ['curl', '-i', '-H', 'Content-Type: application/json', '-X', 'POST', '-d', content, uri]
    result = subprocess.run(command_list, stdout=subprocess.PIPE)    

    return result.stdout

def parse_terms(matches, sentence):
    terms = {}
    #print('matches', matches)
    #print('matches string', str(matches))
    matches_string = str(matches).split('\\n')[-2]
    print(matches_string)
    matches_string = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', matches_string)
    matches_dicts = json.loads(matches_string)['matches']
    for i in range(len(matches_dicts)):
        terms[sentence[matches_dicts[i]['start']:matches_dicts[i]['end']]] = (matches_dicts[i]['start'], matches_dicts[i]['end'])
    
    return terms
    
if __name__ == '__main__':
    sentence = ''
    sentence = ""
    #print(parse_terms(find_matches(sentence.replace('<', '')), sentence))
    print(find_matches(sentence))
