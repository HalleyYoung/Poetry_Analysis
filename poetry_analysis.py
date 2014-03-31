#!/usr/bin/env python2.7
"""
poetry_analysis.py
A poetry analysis program
"""
import word as wd
import poetrytests as pt
import similes as sm
import markup as mp
import helpers as hp
import numpy as np

lines = [] #will contain lines of poetry file
print("This program analyzes poetry.  The poems you wish to analyze should be stored in exactly the following format:\ntitle:[title]\nauthor:[author]\n\n[body of poem]")
main_poem_name = raw_input("Please enter the filename of the poem you wish to analyze.\n")
f = open(main_poem_name, 'rw')
for line in f:
    lines.append(line)

title = (lines[0][7:])[:-1] #Title field of appropriately formatted poetry file
author = (lines[1][8:])[:-1] #Author field of appropriately formatted poetry file
lines = lines[3:]  

word_list = wd.getWordList(lines)

#Literary Devices, measured for the poem being analyzed
simile_list = sm.getSimiles(word_list)
alliteration_list = hp.concat(pt.getAlliterations(word_list))
consonance_list = pt.getConsonance(word_list)
assonance_list = pt.getAssonance(word_list)
rhyme_list = pt.getEndRhymes(word_list) #will need to be fixed

#Some basic tests of meter
isItHaiku = pt.isHaiku(word_list)
isItIambic = pt.mayBeIambic(word_list)

#Other metrics for main poem
tot_words = len(wd.getRealWords(word_list))
average_sentiment = pt.getAverageSentiment(word_list)
lexical_diversity = pt.mtld(word_list)
readability = pt.automated_readability(word_list)
simPerWord = 100*len(simile_list)/tot_words
alliterationPerWord = 100*len(alliteration_list)/tot_words
verb_freq = pt.getVerbFreq(word_list, tot_words)
adj_freq = pt.getAdjFreq(word_list, tot_words)
noun_freq = pt.getNounFreq(word_list, tot_words)
length = tot_words
poem_metrics = [lexical_diversity, length, readability, average_sentiment, simPerWord, alliterationPerWord, verb_freq, adj_freq, noun_freq]
metric_names = ["Lexical Diversity Score", "Poem length (total words)", "Readability Score", "Average sentiment score", "Simile Frequency Score", "Alliteration Frequency Score", "Verb:Total Word Ratio (%)", "Adjective:Total Word Ratio (%)", "Noun:Total Word Ratio (%)"]


#Now, a comparison to other poems on a few criteria
#I realize that I should be able to combine some of this with what I did above without sacrificing efficiency - I will work on that in the future
other_poem_names = raw_input("Please enter the name of other poems you want to compare the first poem too.  The poems should be in the same format, and their names should be separated by a space.\n")
other_poems = other_poem_names.split()
#all of the comparison fields
comp_titles = []
comp_authors = []
comp_diversities = []
comp_lengths = []
comp_readabilities = []
comp_sentiments = []
comp_similes = []
comp_alliterations = []
comp_verb_freqs = []
comp_adj_freqs = []
comp_noun_freqs = []
for i in range(0, len(other_poems)):
    f = open(other_poems[i], "r+")
    lines = []
    for line in f:
        lines.append(line)
    comp_titles.append((lines[0][7:])[:-1])
    comp_authors.append((lines[1][8:])[:-1])
    comp_words = wd.getWordList(lines[3:])
    tot_comp_words = len(wd.getRealWords(comp_words))
    comp_diversities.append(pt.mtld(comp_words))
    comp_lengths.append(tot_comp_words)
    comp_readabilities.append(pt.automated_readability(comp_words))    
    comp_sentiments.append(pt.getAverageSentiment(comp_words))
    comp_similes.append(100*len(sm.getSimiles(comp_words))/tot_comp_words)
    comp_alliterations.append(100*len(pt.getAlliterations(comp_words))/tot_comp_words)
    comp_verb_freqs.append(pt.getVerbFreq(comp_words, tot_comp_words))
    comp_adj_freqs.append(pt.getAdjFreq(comp_words, tot_comp_words))
    comp_noun_freqs.append(pt.getNounFreq(comp_words, tot_comp_words))


#get averages for all metrics
comp_metrics = [comp_diversities, comp_lengths, comp_readabilities, comp_sentiments, comp_similes, comp_alliterations, comp_verb_freqs, comp_adj_freqs, comp_noun_freqs]    
comp_averages = map(np.mean, comp_metrics)
comp_stds = map(np.std, comp_metrics)
    



#Printing the analysis to html    

#checks what attributes the word possesses, and then calculates what colors to visualize the word's attributes
def getColors(word):
    index = word.index
    colors = []
    rhyme_colors = ["009900", "006633", "00CC66", "00FF99", "00FF66"]
    #First, get a list of all the colors the word should be drawn in
    for i in range(0, len(rhyme_list)):
        if index in rhyme_list[i]:
            colors.append("#" + rhyme_colors[i%len(rhyme_colors)])
    if index in simile_list:
        colors.append("red")
    if index in alliteration_list:
        colors.append("blue")
    if index in consonance_list:
        colors.append("orange")


    #then deal with spacing
    raw_word = w.word
    if (index < len(word_list) - 1):
        if (not word_list[index+1].isPunct) and (not raw_word == "-"):
            raw_word += " "    
    #finally, create the html to write the word in the correct colors                
    if len(colors) == 0:
        return raw_word
    if len(colors) == 1:
        return "<font color=" + colors[0] + ">" + raw_word + "</font>"
    else: #make every letter a different color
        word_tag = ""
        for i in range(0, len(raw_word)):
            word_tag += "<font color=" + colors[i%len(colors)] + ">" + raw_word[i] + "</font>"
        return word_tag

#Now put everything else together!
page = mp.page()
page.init(title="Poetic Analysis of " + title, css="poetryanalysislayout.css")
page.br()

page.h1(title, class_="title")
page.h2("By " + author, class_ = "author")

text = ""
for i in range(0, len(word_list)):
    w = word_list[i]
    if w.isEOLN:
        text += "<br />" #line breaks in html
    else:
        text += getColors(w)

page.p(text)

page.h5("Any shade of <font color=\"green\">green</font> indicates a rhyme.")
page.h5("<font color=\"red\">Red</font> indicates a simile.")
page.h5("<font color=\"blue\">Blue</font> indicates alliteration.")
page.h5("<font color=\"orange\">Orange</font> indicates consonance.")

#Meter metrics that don't fit in the table
if (isItHaiku):
    page.h4("The poem is a haiku.")
else:
    page.h4("The poem is probably not a haiku.")    

if (isItIambic):
    page.h4("The poem may be in iambic pentameter")
else:
    page.h4("The poem is probably not in iambic pentameter.")    
    
page.h3("Poem-level Metrics:")

page.table()
page.tr(class_="table-head")
page.td("Metric")
page.td(title)
page.td("Comparison Poems (mean, standard deviation)")
page.tr.close()
for i in range(0, len(metric_names)):
    page.tr(class_="inside_table")
    page.td(metric_names[i])
    if type(poem_metrics[i]) == int:
        page.td(str(poem_metrics[i]))
    else:
        page.td('%.2f' % poem_metrics[i])
    page.td(('%.2f' % comp_averages[i]) + " &plusmn " + ('%.2f' % comp_stds[i]))
    page.tr.close()
page.table.close()

#include a list of poems being compared
page.h6("Comparison poems include:", class_="comparison")
for i in range (0, len(comp_authors)):
    page.h6(comp_titles[i] + " by " + comp_authors[i])

f_out_name = "ComputationalAnalysisOf" + title.replace(' ', '-') + ".html"
f = open(f_out_name, "w")
f.write(page.__str__())
f.close()

#Also need to print css file that html depends on
css = 'body {    font-family: arial;  background-color:#E0E0E0;  }\n\ntable {  position:relative; top:80px solid; background-color: #66CCFF;    border: 3px solid black;    width: 100%;    }\n\n.table-head {font-weight:bold;}\n\ntd {    border: 2px solid;    text-align: center; font-size:150%   }\n\np {    padding-left: 30%;   padding-top:20px; padding-bottom: 80px; font-size:200%;     }\n\nh1 {  text-align: center;    }\n\nh2 { text-align:center }\n\nh3 {text-align:center; font-size:200%; padding-top:80px; }\n\nh4 { text-align:center; position:relative; top:40px;}\n\nh5 {text-align:center; }\n\nh6 {margin-bottom:-15px}\n'
f_css = open("poetryanalysislayout.css", "w")
f_css.write(css)
f_css.close()

print("Your analysis has been written to the file " + f_out_name + " and is viewable within a browser.\n")
