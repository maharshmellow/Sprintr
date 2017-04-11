from formatWord import formatWord

words = []

with open("introbook.txt", "r") as f:
    for line in f:
        for word in line.split():
            words.append(word)

jsFormatWords = formatWord(words)   # should return as list of list -> inject this list into javascript
print(jsFormatWords)
