import sys
import os
import re
import json

def create_kwd_file(fname):
    text_re = re.compile("'([^']*)'=(\d*)")
    type_re = re.compile("([^=]*)=(\d*)")
    
    keywords = {}
    keywords_by_id = {}
    with open(fname, 'r') as f:
        lines = f.readlines()
        for l in lines:
            if l[0] == "'":
                r = re.search(text_re, l).groups()
                keywords_by_id[r[1]] = r[0]
                
        for l in lines:
            if l[0] == "'":
                break
            
            r = re.search(type_re, l).groups()
            
            if r[1] in keywords_by_id:
                text = keywords_by_id[r[1]]
                keywords[r[0]] = text
                
    kwd_fname = os.path.splitext(fname)[0]+'.keywords'
    
    with open(kwd_fname, 'w') as outfile:
        json.dump(keywords, outfile)

if __name__ == "__main__":
    lang = sys.argv[1]
    fname = os.path.abspath(os.path.join(os.getcwd(), '..', lang, lang) + '.tokens')
    create_kwd_file(fname)
