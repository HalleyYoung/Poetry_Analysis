# -*- coding: utf-8 -*-
"""
contains the tests performed on a poem to assess its literary features
"""
#import nltk
from senti_classifier import senti_classifier
import word as wd
from nltk.corpus import brown

#return a list of alliterations, not counting keywords
def isAlliteration(word1, word2):
    return (word1.word[0].lower() == word2.word[0].lower())

def getAlliterations(words):
    alliterations = []
    for i in range(0, len(words) - 1):
        #get the last function word
        if wd.isHighContent(words[i]):
            if wd.isHighContent(words[i+1]):
                if (isAlliteration(words[i], words[i+1])):
                    alliterations.append([i, i+1])            
        #include alliterations spaced one word apart,
        #if the word between is a low-content word and they are in the same sentence    
            elif i < len(words) - 2: #Here it would obviously be more efficient to just create a separate loop for the last few words, but I feel that the increased efficiency is not worth the increased ugliness of the code
                if (wd.isHighContent(words[i+2]) and isAlliteration(words[i], words[i+2])):
                    alliterations.append([i, i+1, i+2]) 
            #finally, include words spaced 3 apart if they are very small function words 
            if i < len(words) - 3:
                if(wd.isFunctionWord(words[i+1].pos) and wd.isFunctionWord(words[i+2].pos) and len(words[i+1].word) < 4 and len(words[i+2].word) < 4):
                    if isAlliteration(words[i], words[i+3]):
                        alliterations.append([i, i+1, i+2, i+3])
    return alliterations

#takes the pronunciation arrays of word1 and word2, returns whether they are a rhyme
#assumption is that something is a rhyme when the last vowel + any consonants following it are the same    
#Right now, I only check the end of the line, but it would be simple enough to apply the same method within lines 
def getEndRhymes(words):
    #get last words of the poem 
    words = wd.getRealWords(words)
    last_words = filter(lambda i: words[i].line != words[i+1].line, range(1, len(words)-1))
    last_words.append(len(words) - 1)
    rhyme_dict = {}
    #create a dict of last sounds 
    for i in range(0, len(last_words)):
        last_word = words[last_words[i]]
        for pron in last_word.pronunciation:
            lastVowel = filter(lambda i: pron[i][0] in "AEIOU", range(0, len(pron)))[0]
            vowel_and_consonants = ''.join(pron[lastVowel:])
            if not vowel_and_consonants in rhyme_dict:
                rhyme_dict[vowel_and_consonants] = [last_word.index]
            else:
                rhyme_dict[vowel_and_consonants].append(last_word.index)
    return filter(lambda i: len(i) > 1, rhyme_dict.values())       
    
#takes the pronunciation arrays of word1 and word2, returns whether they are a rhyme
#assumption is that something is a rhyme when the last vowel + any consonants following it are the same    
def isPerfectRhyme(word1Pronunciations, word2Pronunciations):
    def isPerfect(pron1, pron2): #checks only 2 pronunciations against each other
        #get the last vowel-consonant pair    
        lastVowel1 = filter(lambda i: pron1[i][0] in "AEIOU", range(0, len(pron1)))[0]
        vowel_and_consonants1 = pron1[lastVowel1:]
        lastVowel2 = filter(lambda i: pron2[i][0] in "AEIOU", range(0, len(pron2)))[0]
        vowel_and_consonants2 = pron2[lastVowel2:]
        return(vowel_and_consonants1 == vowel_and_consonants2)
    if (len(word1Pronunciations) == 0) or (len(word2Pronunciations) == 0): #if don't have data on pronunciation
        return False
    else:    
        #get all possible pronunciations of the last syllables
        for pron1 in word1Pronunciations:
            for pron2 in word2Pronunciations:
                if isPerfect(pron1, pron2):
                    return True
        return False

def isConsonance(word1, word2, c): #just using most common pronunciations
    if len(word1.pronunciation) == 0 or len(word2.pronunciation) == 0:
        return False
    else:
        pro1 = word1.pronunciation[0]
        pro2 = word2.pronunciation[0]
        if not c in "SPT": #because plural or past tense words shouldn't count as consonance
            #there should be at least one of the letter in each word, including one that is not the first letter of the word (otherwise it would be alliteration)
            if (pro1[1:].count(c) > 0 and pro2.count(c) > 0) or (pro2[1:].count(c) > 0 and pro1.count(c) > 0):
                return True
        else:
            if ((pro1[1:])[:-1].count(c) > 0 and pro2[:-1].count(c) > 0) or ((pro2[1:])[:-1].count(c) > 0 and pro1[:-1].count(c) > 0):
                return True  
    return False   

  
"""Right now, going with definition of consonance where there is at least one of the same letter in 2 adjacent, high-content words 
and that the total instances of that letter is greater than 2"""
def getConsonance(words):
    def isConsonance(word1, word2, c): #just using most common pronunciations
        if len(word1.pronunciation) == 0 or len(word2.pronunciation) == 0:
            return False
        else:
            pro1 = word1.pronunciation[0]
            pro2 = word2.pronunciation[0]
            if not c in "SPT": #because plural or past tense words shouldn't count as consonance
                #there should be at least one of the letter in each word, including one that is not the first letter of the word (otherwise it would be alliteration)
                if ((pro1[1:].count(c) > 0 and pro2.count(c) > 0) or (pro2[1:].count(c) > 0 and pro1.count(c) > 0)) and ((pro1.count(c)+pro2.count(c))>2):
                    return True
            else:
                if (((pro1[1:])[:-1].count(c) > 0 and pro2[:-1].count(c) > 0) or (pro2[1:])[:-1].count(c) > 0 and pro1[:-1].count(c) > 0) and ((pro1.count(c)+pro2.count(c))>2):
                    return True  
        return False           
    indices = []
    consonants = "KMNDZSPT"
    for i in range(0, len(consonants)):
        c = consonants[i]
        for j in range(0, len(words) - 2): 
            if (wd.isHighContent(words[j])):
                if wd.isHighContent(words[j+1]):
                    if (isConsonance(words[j], words[j+1], c)):
                        indices.append(j)
                        indices.append(j+1)
                elif (wd.isHighContent(words[j+2])):
                        if (isConsonance(words[j], words[j+2], c)):
                            indices.append(j)
                            indices.append(j+1)
                            indices.append(j+2)

    return list(set(indices))   
    #check each line for consonants, see if you see similar consonants


#getAssonance returns the indices of words if a vowel sound is repeated at least three times in a string of 4 words) 
def getAssonance(words):
    words = wd.getRealWords(words)
    indices = []
    vowel_phonemes = ["AA", "AE", "AH", "AO", "AW", "AY", "EY", "IH", "IY", "OW", "OY", "UH", "UW"]
    def vowel_freq(word, vowel):
        def stripPronunciation(pronunciation): #this is only necessary because of the way the cmudict output is formatted - it includes subvariants of each phoneme, this strips them
            pronunciations = []
            for phoneme in pronunciation:
                if phoneme[0] in "AEIOU":
                    pronunciations.append(phoneme[:-1])
                else:
                    pronunciations.append(phoneme)
            return pronunciations    
        pronunciation_starts = map(stripPronunciation, word.pronunciation)
        if len(word.pronunciation) > 0:
            return max(map(lambda i: i.count(vowel), pronunciation_starts))
        else:
            return 0
    for vowel in vowel_phonemes:
        vowel_freqs = map(lambda i: vowel_freq(i, vowel), words)
        many_vowels = filter(lambda i: sum(vowel_freqs[i:i+4]) >= 3, range(0, len(words))) #get sections with many vowels
        print(vowel)
        print(many_vowels)
        for i in range(0, len(many_vowels)): #but just add indices of words that actually have vowels
            for j in range(many_vowels[i], many_vowels[i] + 3):
                if vowel_freqs[j] > 0 and (not (words[j].index in indices)):
                    indices.append(words[j].index)
                    print(words[j].word + "vowel: " + vowel)
    return indices               
    
"""
Automated readability is one of several metrics used to judge a text's sophistication.
It only uses characters/word and words/sentence as a proxy for literary complexity.
"""    
def automated_readability(words):
    sentences = words[-1].sentence
    word_count = len(words)
    chars = sum(map(lambda i: len(i.word), words)) #need syllables!
    return (4.71*chars/word_count) + (0.5*word_count/sentences) - 21.43   
    
"""
It is very difficult to find a measure of lexical diversity (amount of variation in word choice)
that is not heavily influenced by text length.  Mean textual lexical diversity seems to be 
the least influenced by text length, but it also may not be so meaningful with very short texts.
MTLD measures the average length of strings above a certain type-token ratio (ratio of unique words:total words).
For a more detailed description of the algorithm, see: http://vli-journal.org/issues/01.1/issue01.1.10.pdf
Higher MTLD indicates greater lexical diversity.
"""    
def mtld (words):
    words_only = map(lambda i: i.word, words)
    #ttr = ratio of unique words to total words.  It is needed to calculate mtld
    def ttr(tokens):
        return len(set(tokens))/len(tokens)
    def one_way(wds):
        ttr_current = 1.0
        count = 0.0
        cutoff = .72
        start = 0    
        for x in range(1, len (wds) + 1):
            ttr_current = ttr(wds[start:x]) 
            if (ttr_current < cutoff): #Has the ttr gone below the cutoff?
            #if the ttr dips below the cutoff after less than 10 tokens, count isn't affected,
            #with the assumption that meaningless function words are being repeated
                   if (x - start >= 10): 
                       count += 1.0
                   start = x 
            else:
                if (x == len(wds)):
                    count += (1 - ttr_current)/(1 - cutoff)             
        if count > 0:
            return (len (wds) + 0.0)/count 
        else:
            return 0
    return (one_way(words_only)+one_way(words_only[::-1]))/2        

#returns percentage of word tokens that are verbs.  I included the number of words as a parameter
#simply because it is used so often that it seemed more efficient to only have it calculated once
def getVerbFreq(words, tot_words):
    return (100*len(filter(wd.isVerb, words))+0.0)/tot_words
    
    
#returns percentage of word tokens that are adjectives.  
def getAdjFreq(words, tot_words):
    return (100*len(filter(wd.isAdjective, words))+0.0)/tot_words    
    

#returns percentage of word tokens that are nouns.  
def getNounFreq(words, tot_words):
    return (100*len(filter(wd.isNoun, words))+0.0)/tot_words       

#returns a list of doubles corresponding to the net sentiment of each sentence
#Sentiment data taken from the senti_wordnet, word disambiguation from brown corpus 
#(within sentiment classifier library available at https://github.com/kevincobain2000/sentiment_classifier/blob/master/scripts/senti_classifier)
def getSentiment(words):
    sentences = wd.getSentences(words)
    sentiments = []
    for sentence in sentences:
        pos, neg = senti_classifier.polarity_scores(map(lambda i: i.word, sentence))
        sentiments.append(pos - neg)
    return sentiments

#Average sentiment of every sentence
def getAverageSentiment(words):
    sent = getSentiment(words)
    return sum(sent)/len(sent)    
      


#Return a list of syllables, based on the assumption that number of vowel phonemes = number of syllables
def getTotalSyllablesInWord(pronunciation):
    def isVowel(phoneme):
        return (phoneme[0] in "AEIOU")
    return len(filter(isVowel, pronunciation))  


#Returns first pronunciation in cmudict dictionary for a word object
def getFirstPronunciation(word):
    if len(word.pronunciation) > 0:
        return word.pronunciation[0]
    else:
        return []   

    
#Checks if the poem could be a haiku, based on the number of syllables
def isHaiku(words):
    words = filter(lambda i: not i.isPunct and not i.isEOLN, words)
    lines = map(lambda i: filter(lambda j: j.line == i, words), range(0, words[-1].line + 1))
    lines = filter(lambda i: len(i) > 0, lines)
    #First, make sure there are only three lines
    if len(lines) != 3:
        return False
    #Now, check if the lines follow the correct pattern
    #Assumption is that if they are a haiku, the first line will have 5 syllables, then 7, and then 5   
    pronunciations = map(lambda i: map(getFirstPronunciation, i), lines)
    linetotals = map(lambda i: sum(map(getTotalSyllablesInWord, i)), pronunciations)
    if linetotals[0] == 5 and linetotals[1] == 7 and linetotals[2] == 5:
        return True
    return False    

#returns true if every line has 10 syllables, or if >80% have 10 and >85% have 9,10 or 11
def mayBeIambic(words):
    words = filter(lambda i: not i.isPunct and not i.isEOLN, words)
    lines = map(lambda i: filter(lambda j: j.line == i, words), range(0, words[-1].line + 1))
    lines = filter(lambda i: len(i) > 0, lines)
    pronunciations = map(lambda i: map(getFirstPronunciation, i), lines)
    linetotals = map(lambda i: sum(map(getTotalSyllablesInWord, i)), pronunciations)
    if all(map(lambda i: i == 10, linetotals)): #If all lines have 10 syllables
        return True
    else: #if 80% of lines have 10 syllables and 10% have between 9 and 11 syllables (to avoid problems with cmudict not recognizing a word)
        if (linetotals.count(10) > int(0.8*len(linetotals))) and (linetotals.count(10)+linetotals.count(9)+linetotals.count(11) > int(0.85*len(linetotals))):
            return True
    return False

    
"""returns the words that are least frequently seen in a standard corpus of romance novels
(which was the closest I could find to poetry)
I ended up not including this in the program: It takes too long to run, and too many words are not
included in the corpus.  However, I'm keeping it here because at some point, I would like to incorporate 
corpus data into the analyzer
"""
def uncommon_words(words):
    indices = []
    corpus_words = brown.words(categories='romance')
    tot_corpus_words = len(corpus_words) + 0.0
    content_words = filter(wd.isHighContent, words)
    #take any words that account for less than 0.00005% of brown corpus
    for word in content_words:
        if (corpus_words.count(word.word)/tot_corpus_words) < 0.000005:
            indices.append(word.index)
    return indices    