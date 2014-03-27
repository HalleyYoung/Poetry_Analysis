# -*- coding: utf-8 -*-
"""
word.py
contains Word object definition and general function pertaining to word objects
"""
from nltk.corpus import cmudict
import nltk

#class for containing word and all of its attributes  
def tokens(words):
    return map (lambda i: i.word, words)
  
class Word:
    def __init__(self, word, pronunciation, isPunct, line, index):
        self.word = word
        self.line = line #which number line
        self.sentence = -1 #which number sentence
        self.pos = "" #part of speech
        self.pronunciation = pronunciation
        self.isFunctionWord = False
        self.isPunct = isPunct
        self.isEOLN = False
        self.index = index

#returns 2-D list of sentences, with EOLN tokens filtered out
def getSentences(words):
     return map(lambda i: filter(lambda j: j.sentence == i and (not j.isEOLN), words), range(0, words[-1].sentence))

#This slows things down a bit, but pretty necessary for a poetry analyzer...
def getPronunciation(word, d):
    if word in d:
        return d[word]
    else:
        return []

#crude estimate of whether something is pronunciation
def isPunct(word):
    return all(map(lambda i: not i.isalnum(), word))

#I include the following types of words as high-content (as opposed to determinants like "the" or pronouns, which often should not be included in an analysis)
#Adverbs, adjectives, all types of verbs except for existential verbs, all types of nouns except for pronouns, interjections
#I also skip any word less than four letters, to decrease false positives from an imperfect part of speech tagger
def isHighContent(word):
    return (word.pos in ["ADJ", "NUM", "NP", "ADV", "VD", "VG", "VN", "N", "P", "V", "UH"] and len(word.word) > 3)


#includes who/what type words, conjunctions, pronouns, determinants (a, the, etc.), modal auxiliary (can, must, should, etc)
def isFunctionWord(pos_tag):
    function_tags = ["WH","CNJ","TO","PRO","DET","MOD","P"]     
    return (pos_tag in function_tags)
    

#returns whether a Word object is a verb
def isVerb(word):
    return (word.pos in ["VD", "VG", "VN", "V"])

#returns whether a Word object is an adjective
def isAdjective(word):
    return (word.pos in ["ADJ", "NUM"])
    
#returns whether a Word object is a noun
def isNoun(word):
    return (word.pos in ["N", "NP", "PRO"])    
    
def getRealWords(words):
    return filter(lambda i: not(i.isPunct or i.isEOLN), words)    
    
#tokenizing lines into individual words
def tokenize(lines):
    punc = "-/~,.-;!|\n"
    words = []
    cur_word = ""
    for c in lines:
        if (c == ' '):
            if (len(cur_word) > 0): #add current word to words, start a new word
                words.append(cur_word)
                cur_word = ""
        elif (c in punc):
            if (len(cur_word) > 0): #again, add current word, start new words
                words.append(cur_word)
                cur_word = ""
            words.append(str(c)) #and add punctuation
        else:
            cur_word += c
    if (len(cur_word) > 0):
        words.append(cur_word)
    return words            


#Builds a list of Word objects out of unformatted code from a text file    
def getWordList(lines):
    word_objects = []
    d = cmudict.dict()

    def getPOS(words):        
        #I use simplified tags so that it is easier to parse the grammar for my simile checker
        pos =[(word, nltk.tag.simplify.simplify_wsj_tag(tag)) for (word, tag) in nltk.pos_tag(words)]
        return pos    
    
    tokenized = map(lambda i: tokenize(i), lines) #tokenizes string of words to individuals words/punctuation

    raw_words = []
    #create 1-D list from list of lines
    for i in range(0, len(tokenized)):
        raw_words += tokenized[i]

    
    #create a list of word objects (although right now you don't have all of the data about the words)
    line = 0
    for i in range(0, len(raw_words)):
        raw_word = raw_words[i]
        w = Word(index=i, word=raw_word, pronunciation=getPronunciation(raw_word.lower(), d), line = line, isPunct = isPunct(raw_word))
        word_objects.append(w)
        if (raw_word == "\n"):
            line += 1
        
    
    #Now: get sentence-level data
    #First, split sentences so that every element in an array is either a sentence or ["\n"]
    start_word = 0
    sentences = []
    for i in range(0, len(raw_words)):
        current = raw_words[i]
        if (current == "."):
            sentences.append(raw_words[start_word:i + 1])
            start_word = i + 1
        elif (current == "\n"):
            if (start_word != i):
                sentences.append(raw_words[start_word:i])
            sentences.append([current])
            start_word = i + 1
    if start_word < len(raw_words):
        sentences.append(raw_words[start_word:])
    
    pos_sentences = []
    #Get the position data for each sentence
    for sent in sentences:
        if sent[0] == "\n":
            pos_sentences += [("\n", "EOLN")]
        else:
            pos_sentences += getPOS(sent)
            
    sentence = 0            
    for i in range(0, len(word_objects)):
        pos = pos_sentences[i][1]
        if word_objects[i].isPunct:
            word_objects[i].pos = "PUNC"
        else:    
            word_objects[i].pos = pos
        word_objects[i].isFunctionWord = isFunctionWord(pos)
        word_objects[i].sentence = sentence
        word_objects[i].isEOLN = pos == "EOLN"
        if (pos == '.'):
            sentence += 1
        
    return word_objects

    
    
    
    
    
    
    
    
    
    
    