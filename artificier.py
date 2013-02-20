#date stuff

import urllib
import re
import nltk
import json
from bottle import route,post,run,request,static_file


def load_mapping(pos):
    return dict([(word,year) for (year,tab,word) in 
                    [x.partition('\t') for x in 
                        open('neologisms/neologisms.' + pos).read().split('\n')]])


def lemmatize(word,pos):
    """Lemmatize the word as appropriate for the part of speech."""
    #If the type is unknown, ignore it
    types = {'VB':'v', 'NN': 'n'}
    return lmz.lemmatize(word,types[pos]) if pos in types else word

def get_year(word,pos):
    """Look the normalized word up in the history list."""
    types = {'VB':verbs, 'NN': nouns, 'JJ': adjectives, 'RB': adverbs }
    return types[pos][word] if pos in types and word in types[pos] else None

def classify(word,year):
    cent = "" #century
    if not year:
        return word
    else:
        cent = 'c' + str(int(year)+99)[0:2] #c20, c19, etc.
    return '''<a href="http://dictionary.reference.com/browse/%s" target="blank">
              <span class="dated date-%s" title="%s">
              %s</span></a>''' % (word,cent,str(year),word)

@post('/date')
def calculate_dates():
    """Take in the input and output formatted HTML with classes for dates."""
    input = urllib.unquote(str(request.forms.get('text')))
    print input

    output = ""
    max_date = 0
    pps = input.split('\n')
    for pp in pps: 
        sents = nltk.tokenize.sent_tokenize(pp)
        output += '<p>'
        for sent in sents:
            #print sent
            tags = nltk.pos_tag(nltk.word_tokenize(sent))
            # Remove the second half of contractions and punc-only tokens
            tags = [t[1] for t in tags if not (re.match("[^A-z]",t[0]) or "'" in t[0])]
            words = sent.split()
            tags = zip(words,tags)
            for (ww,pos) in tags:
                #print "%s\t%s" % (ww,pos)
                pos = pos[0:2] #Don't care about details
                canon = lemmatize(ww.strip('[^A-z]').lower(),pos)
                year = get_year(canon,pos)
                if year:
                    #print "%s\t%s" % (ww,year)
                    if int(year) > max_date: max_date = int(year)
                output += ' ' if ww not in '.,;)!?:' else ''
                output += classify(ww,year)
        output += '</p>\n\n'
    print max_date
    return {'text':urllib.quote(output), 'max_year': max_date}

@route('/')
def index():
    return static_file('index.html',root='./static')

@route('/<filename:path>')
def static(filename):
    return static_file(filename,root='./static')

lmz = nltk.stem.wordnet.WordNetLemmatizer()
nouns = load_mapping('nn')
verbs = load_mapping('vb')
adjectives = load_mapping('jj')
adverbs = load_mapping('rb')

run(reloader=True,debug=True,port=2323,host='0.0.0.0',server='cherrypy')
