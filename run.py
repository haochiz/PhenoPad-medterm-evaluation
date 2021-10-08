# python3.5+
import os

import transcripts
import extract_terms as extract

def main(path, fn):
    all_ref_terms = []
    all_hyp_terms = []
    
    result_f = open('eval_results/sent_by_sent/final/' + fn, 'w')
    # load file
    lines = transcripts.load(fn, path)
    sent_pairs = transcripts.get_sent_pairs(lines)
    total_terms = 0
    total_true_positive = 0
    total_false_positive = 0
    # get med terms for each sent pairs
    for pi, pair in enumerate(sent_pairs):
        print(pair[0])
        print(pair[1])
        
        # extract terms
        ref_terms = extract.parse_terms(extract.find_matches(pair[0]), pair[0])
        hyp_terms = extract.parse_terms(extract.find_matches(pair[1]), pair[1])
        # record terms
        if len(ref_terms) > 0: all_ref_terms = extend_terms(all_ref_terms, ref_terms)
        if len(hyp_terms) > 0: all_hyp_terms = extend_terms(all_hyp_terms, hyp_terms)
        # log acc
        print(ref_terms, hyp_terms)
        print(count_correct(ref_terms, hyp_terms))
        true_positive, false_positive, num_terms = count_correct(ref_terms, hyp_terms)
        total_true_positive += true_positive
        total_false_positive += false_positive
        total_terms += num_terms
        print('Sentence {}: prcision = {}/{}, recall = {}/{}'.format(pi, true_positive, true_positive+false_positive, true_positive, num_terms))
        result_f.write('Sentence {}: prcision = {}/{}, recall = {}/{}\n'.format(pi, true_positive, true_positive+false_positive, true_positive, num_terms))
        result_f.flush()
        ref_terms_string = format_terms_string(ref_terms, pair[0][5:])
        hyp_terms_string = format_terms_string(hyp_terms, pair[1][5:])
        # log terms
        print('REF      : ' + pair[0][5:])
        print('REF Terms: ' + ref_terms_string)
        print('HYP      : ' + pair[1][5:])
        print('HYP Terms: ' + hyp_terms_string)        
        result_f.write('REF      : ' + pair[0][5:] + '\n')
        result_f.write('REF Terms: ' + ref_terms_string + '\n')
        result_f.write('HYP      : ' + pair[1][5:] + '\n')
        result_f.write('HYP Terms: ' + hyp_terms_string + '\n\n')        
        result_f.flush()
    session_true_positive, session_false_positive, session_terms = count_correct_session(all_ref_terms, all_hyp_terms)

    print('SESSION REF TERMS: {}'.format(', '.join(list(set(all_ref_terms)))))
    print('SESSION HYP TERMS: {}'.format(', '.join(list(set(all_hyp_terms)))))
    result_f.write('SESSION REF TERMS: {}\n'.format(', '.join(list(set(all_ref_terms)))))
    result_f.write('SESSION HYP TERMS: {}\n'.format(', '.join(list(set(all_hyp_terms)))))
    print('Precision = {}/{}, Recall = {}/{}\n'.format(session_true_positive, session_true_positive+session_false_positive, session_true_positive, session_terms))
    result_f.write('Precision = {}/{}, Recall = {}/{}\n'.format(session_true_positive, session_true_positive+session_false_positive, session_true_positive, session_terms))
    result_f.flush()
    result_f.close()

def count_correct(ref_terms_, hyp_terms_):
    ref_terms = [term[0] for term in ref_terms_]
    hyp_terms = [term[0] for term in hyp_terms_]
    true_positive = 0
    false_postive = 0
    total_ref_terms = len(ref_terms)
    for term in hyp_terms:
        if term in ref_terms:
            true_positive += 1
            ref_terms.remove(term)
        else:
            false_postive += 1
     
    return true_positive, false_postive, total_ref_terms

def count_correct_session(ref_terms, hyp_terms):
    ref_terms = list(set(ref_terms))
    hyp_terms = list(set(hyp_terms))
    true_positive = 0
    false_postive = 0
    for term in hyp_terms:
        if term in ref_terms:
            true_positive += 1
        else:
            false_postive += 1

    return true_positive, false_postive, len(ref_terms)

def extend_terms(spider, fly):
    for term in fly:
        spider.append(term[0])
    return spider

def format_terms_string(terms, sentence):
    string = ' ' * len(sentence)
    for term in terms:
        string = string[:term[1][0]-5] + term[0] + string[term[1][1]-5+1:]

    return string
        

if __name__ == '__main__':
    transcripts_path = ''
    file_list = os.listdir(transcripts_path)
    for fn in file_list:
        main(transcripts_path, fn)
