# -*- coding: utf-8 -*-
"""
similes.py
simile detection functions
"""
import nltk
import helpers as hp
import word as wd

#This is a very crude guesstimator for possible similes, where possible instances are only checked for grammar
#It returns the index of a possible simile
def getSimiles(words):
    #First, get an array of words grouped by sentences
    sentences = wd.getSentences(words)
    
    #Tokenize sentences, keeping index data
    tokenized = map(lambda i: tokenizeSent(i, {"like", "as"}), sentences)
    similes = map(parseSimile, tokenized)
    return hp.concat(similes)      
 
#Use to get an array of mostly part of speech objects, but reserving a number of keywords.  
#This is useful for cases where you want to check if sentences are using a word in a particular way;
#for instance, for guessing whether like is used as a simile or not.  
def tokenizeSent(sent, keywords):
    def changeWord(word):
        if word.word in keywords:
            return word.word
        else:
            return word.pos
    return (map(lambda i: (changeWord(i), i.index), sent))
   
#Simile parser   
#takes a list of tokens and their indices in form [(token, index)]   
def parseSimile(tokensWithIndices):
    #The grammar used to check a simile
    grammar = nltk.parse_cfg("""
    S -> NP "like" NP | "ADJ" "like" "NP" | NP V "like" NP | "EX" "like" "NP" | NP "as" "ADJ" "as" NP | V "as" "ADJ" "as" NP |OTH
    NP -> N | "ADJ" N | "DET" NP 
    N -> "NP" | "PRO" | "N"
    V -> "VD" | "V" | "VG"
    OTH -> "OTH" "PUNC" "FW" "WH" "TO" "NUM" "ADV" "VD" "VG" "L" "VN" "N" "P" "S" "EX" "V" "CNJ" "UH" "PRO" "MOD"  
    """)  
    tokens = map(lambda i: i[0], tokensWithIndices)
    indices = map(lambda i: i[1], tokensWithIndices)
    parser = nltk.ChartParser(grammar)
    simile_indices = []
    start_token = 0
    while (start_token < len(tokens) - 2):
        end_token = start_token + 2 #can't have simile smaller than 4 words
        simile = False
        while ( (not simile) and (end_token <= len(tokens))):
            if (len(parser.nbest_parse(tokens[start_token:end_token])) > 0): #If a parse tree was formed
                simile_indices.extend(indices[start_token:end_token])
                start_token = end_token
                simile = True            
            else:    
                end_token += 1
        start_token += 1
    return simile_indices
