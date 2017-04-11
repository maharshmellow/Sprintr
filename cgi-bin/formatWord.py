# This file formats a list of words in a format that will be used by the Javascript file
# Each word will be separeted into three subsections: [left, pivot, right]
# Empty spaces will be filled with &nbsp

def formatWord(words):
    """words = list of word"""

    returnList = []

    for word in words:
        length = len(word)

        # get pivot position
        if length <= 1:
            pivot = 0
        elif length <= 5:
            pivot = 1
        elif length <= 9:
            pivot = 2
        else:
            pivot = 3

        leftSubstring = word[0:pivot]
        pivotString = word[pivot]
        rightSubstring = word[pivot+1:]

        # add whitespace character for javascript
        leftSubstring = ("&nbsp;"*(5-len(leftSubstring))) + leftSubstring # only have 5 characters for the left section
        rightSubstring = rightSubstring[:8] + ("&nbsp;"*(8-len(rightSubstring)))    # remove the characters after the 8th position since there isn't enough space

        returnList.append([leftSubstring, pivotString, rightSubstring, min(length, 14), getPunctuationID(word)])

    return(returnList)

def getPunctuationID(word):
    """
    if there are multiple punctuation marks in the word, the ID returned depends on the first one that appears in the list
    """

    punctuationMarks = [".", "!", "?", ",", "-", ":"]
    for mark in punctuationMarks:
        if mark in word:
            return(punctuationMarks.index(mark) + 1)

    return(0)   # no punction marks
