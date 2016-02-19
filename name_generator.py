#!/usr/bin/python
# coding=utf-8

consonants=['p','b','t','d','t͡ʃ','d͡ʒ','k','ɡ','f','v','θ','ð','s',
            'z','ʃ','ʒ','x','h','m','n','ŋ','l','r','w','j','hw']
marginals=['ʔ']
reduced_vowels=['ə','ɪ̈ (ə)','ʊ̈ (ə)','ɵ (ə)','ɚ (ə)']
vowels=['æ','ɑː','ɒ','ɔː','ə','ɨ','ɪ','i','iː','eɪ','ɛ','ɜr','ər','ʌ','ʊ','uː',
        'juː','aɪ','ɔɪ','oʊ','aʊ','ɑr','ɪər','ɛər','ɔr','ɔər','ʊər','jʊər']

from random import choice, gauss, random, seed

classes=[marginals,reduced_vowels,consonants,vowels]

def getPossible(word):
    if len(word) == 0:
        return {0.50: consonants,
                1.00: vowels}
    if word[-1] in vowels:
        return {0.05: marginals,
                0.75: consonants,
                1.00: vowels}
    if word[-1] in consonants:
        if len(word) == 1 or word[-2] in consonants:
            return {0.05: marginals,
                    0.25: consonants,
                    1.00: vowels}
        else:
            return {0.05: marginals,
                    0.60: consonants,
                    1.00: vowels}
    #last letter was marginal or reduced vowel
    return {0.00: marginals,
            0.75: consonants,
            1.00: vowels}

def nextChar(probs):
    n = random()
    for p,c in probs.items():
        if n < p:
            return choice(c)
    return ''

def next(medianLength=7,stddev=3):
    l = int(gauss(medianLength,stddev))
    while l < 2:
        l = int(gauss(medianLength,stddev))
    name = ''
    trans = ['']
    while len(name) < l:
        nc=nextChar(getPossible(name))
        name += nc
        trans = add(trans, translate(nc,american))
    return name, trans

def printResult(res):
    base, trans = res
    print base
    for t in trans:
        print t

def nextSyll(odds1=1,odds2=1,odds3=1):
    n = random() * (odds1+odds2+odds3)
    if n < odds1:
        return choice(vowels)
    elif n < odds1 + odds2:
        if random() < 0.5:
            return choice(vowels)+choice(consonants)
        else:
            return choice(consonants)+choice(vowels)
    else:
        n=random()
        if n < 1/3.0:
            return choice(vowels)+choice(consonants)+choice(consonants)
        elif n < 2/3.0:
            return choice(consonants)+choice(vowels)+choice(consonants)
        else:
            return choice(consonants)+choice(consonants)+choice(vowels)
        
def next2(median=3,stddev=1,**args):
    name = ''
    for i in range(0,int(round(gauss(median,stddev))) or 1):
        name += nextSyll(**args)
    return name

def translate2(word, translations):
    trans=['']
    subs=list(translations.items())
    subs.sort(key=(lambda a: len(a)), reverse=True)
    while word:
        word, trans = findAndReplace(word,trans,subs)
    return trans

def findAndReplace(word, trans, subs):
    for s,t in subs:
        if word.startswith(s):
            return word.replace(s, '', 1), add(trans, t)
    else:
        return word[1:], add(trans, word[0])

def translate(c,translations):
    trans=['']
    if c in translations:
        trans = add(trans, translations[c])
    else:
        trans = add(trans, c)
    return trans

def add(bases,chars):
    return [b+c for b in bases for c in chars]

american={
    't͡ʃ': ('ch',),
    'd͡ʒ': ('g','j','dg'),
    #'k': 'k',
    #'f',
    'ɡ': ('g',),
    'θ': ('th',),
    'ð': ('th',),
    'ʃ': ('sh','t','ss'),
    'ʒ': ('s','t','ge'),
    'x': ('ch',),
    'ŋ': ('ng','n'),
    'l': ('l','ll'),
    'j': ('y',),
    'hw': ('wh',),
    'ʔ': ("'",'-'),
    'æ': ('a',),
    'ɑː': ('a',),
    'ɒ': ('o',),
    'ɔː': ('aw','au'),
    'ə': ('a',),
    'ɨ': ('e',),
    'ɪ': ('i',),
    'i': ('y',),
    'iː': ('ee','ea'),
    'eɪ': ('ay','ai','ei','ey'),
    'ɛ': ('e',),
    'ɜr': ('ur','er','ear','i'),
    'ər': ('er',),
    'ʌ': ('u','o','oo'),
    'ʊ': ('u','oo'),
    'uː': ('ou','ew'),
    'juː': ('u','ew','ewe'),
    'aɪ': ('y','igh'),
    'ɔɪ': ('oi','oy'),
    'oʊ': ('o','ou','ow','oa','oe'),
    'aʊ': ('ou','ow'),
    'ɑr': ('ar',),
    'ɪər': ('eer','ere'),
    'ɛər': ('are','ere','ear'),
    'ɔr': ('ar','or'),
    'ɔər': ('or','ore','oar'),
    'ʊər': ('oor','our'),
    'jʊər': ('ure','eur')}

last=''

def printNext(**args):
    global last
    last,trans = next(**args)
    printResult( (last,trans) )

def printNext2(**args):
    global last
    last = next2(**args)
    print last
    for t in translate2(last, american):
        print t
    

def save():
    f= open('names.list','a')
    try:
        f.write(last+'\n')
    finally:
        f.close()

def go():
    import sys, tty, termios
    stdin=sys.stdin.fileno()
    old_attrs=termios.tcgetattr(stdin)
    try:
        c = '\n'
        while c not in 'qd':
            if c in ' \nn':
                printNext()
            elif c == 'm':
                printNext2()
            elif c == 's':
                save()
                print 'saved', last
            tty.setraw(stdin)
            c=sys.stdin.read(1)
            termios.tcsetattr(stdin, termios.TCSADRAIN, old_attrs)
    finally:
        termios.tcsetattr(stdin, termios.TCSADRAIN, old_attrs)

if __name__ == '__main__':
    go()
