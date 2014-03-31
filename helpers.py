"""
helpers.py
helper functions
"""

#Turns a two-d list into a 1-D list.
def concat(xss):
    return list(set([x for xs in xss for x in xs]))

