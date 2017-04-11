#!/home/maharshmellow/anaconda3/bin/python3.5
# -*- coding: UTF-8 -*-

import cgitb
import cgi
import os
from formatWord import formatWord
import pickle
from subprocess import Popen, PIPE, DEVNULL

cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()
# sets the max length of the post request (in bytes) -- used to limit uplaod size
cgi.maxlen = 1000000

def main():
    try:
        form = cgi.FieldStorage()
    except:
        print(10)   # file too large error
    else:
        f = form["upload"]
        email = form["email"].value
        bookName = form["code"].value

        if f.filename:
            if validateFile(f) and saveUploadedFile(f, bookName) and convertFile(f, bookName):
                # success - return a success message
                print(1)        # success
            else:
                print(2)    # saving / conversion error
        else:
            print(0)        # upload error

def validateFile(f):
    if getExtension(f) in [".txt", ".epub", ".mobi", ".pdf", ".rtf", ".odt"]:
        return(True)
    else:
        return(False)

def saveUploadedFile(f, bookName):
    try:
        open(bookName+getExtension(f), "wb").write(f.file.read())
        return(True)
    except:
        return(False)

def convertFile(f, bookName):
    # convert file to .txt using calibre ebook-convert
    uploadedFile = bookName + getExtension(f)
    outputFile = bookName + ".txt"
    textFileUploaded = True

    if getExtension(f) != ".txt":
        textFileUploaded = False
        try:
            # uses calibre to convert the file to a text file - waits until complete
            process = Popen(["ebook-convert", uploadedFile, outputFile], stdout=DEVNULL, stderr=DEVNULL).wait() # reditecting the output to DEVNULL removes any errors or any output that the function may produce
        except:
            return(False)

    # read file and convert into a javascript friendly list format
    words = []
    with open(bookName + ".txt", "r", encoding="utf-8") as f:
        for line in f:
            for word in line.split():
                words.append(word)

    jsFormatWords = formatWord(words)   # convert list to JS injectable list

    # save list to .obj file using pickle
    try:
        filehandler = open("/var/www/books/" + bookName + ".obj", "wb")
        pickle.dump(jsFormatWords, filehandler)
        filehandler.close()
    except:
        return(False)

    # delete the uploaded file and the converted text file
    os.remove(uploadedFile)
    if not textFileUploaded:
        os.remove(outputFile)   # only have an output file when NOT uploading .txt

    return(True)


def getExtension(f):
    return(os.path.splitext(f.filename)[1])

main()
