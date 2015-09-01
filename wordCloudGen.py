import string
from htmlFunctions import *

def readStop(file):
    '''Reads the incoming file and splits all the words into their own segment
    in an array. Meant to parse the stopwords document to get the most frequently
    used words.
    file - The file requesting to be read
    return - An array of all words (nonunique) in file '''
    fileref = open(file, 'r')
    stopwords = []
    for line in fileref:
        word = line.split()
        stopwords.append(word[0])
    return stopwords

def readDocument(stopWords, documentName):
    '''Reads the actual document intended to form a word cloud by performing
    simple manipulations to get it ready for data extraction.
    stopWords - An array of the words intended to be ignored by the program
    documentName - the document to form the word cloud
    Return - A list of all words in documentName (excluding stopwords)'''
    fileref = open(documentName, 'r')

    #turns document into one giant string
    docToString = ""
    for line in fileref:
        docToString = docToString + line

    #removes all punctuation from the text.
    for punct in string.punctuation:
        docToString = docToString.replace(punct, "")
        
    docToString = docToString.lower()

    wordlist = docToString.split()

    #removes all stopwords from the text
    for word in stopWords:
        while word in wordlist:
            wordlist.remove(word)

    return wordlist
    
def countWords(name):
    '''Counts all words in the text
    name - name of the document to parse
    Return - a dictionary of key-value pair "word:frequency"'''
    wordCounter = {}

    #simple for-loop to increment frequency of a word (if exists) or to initalize
    #frequency to 1 for first occurance
    for word in name:
        if word in wordCounter:
            wordCounter[word] = wordCounter[word] + 1
        else:
            wordCounter[word] = 1
    return wordCounter

def countToTuples(countDict):
    '''Turns the dictionary from countWords into a tuple pair of relation
    (word, frequency). This is a remnant from the class assignment requirement
    but kept for console output.
    countDict - the dictionary of word:frequency value pairs from countWords
    Return - a tuple with relation (word, frequency)'''
    tupleList = []
    for word in list(countDict.keys()):
        wordTuple = (countDict[word], word)
        tupleList.append(wordTuple)
    return tupleList

def printFrequency(countTuple, name):
    '''Prints the frequency to the console
    countTuple - the tuple generated from countToTuples
    Return - nothing'''
    print('++++++++++++')
    print('%-5s: words in frequency order as count:word pairs'%(name))
    countList = []
    for tup in countTuple:
        countList.append(str(str(tup[0]) + ':' + str(tup[1])))

    for i in range(0, len(countTuple), 4):
        print('%-15s%-15s%-15s%-15s'%(countList[i], countList[i+1], countList[i+2], countList[i+3]))

def makeBoxHTML(nameTuple, name):
    '''Feeds the info to be converted to html to print out the actual Word Cloud
    nameTuple - the tuple generated from countToTuples
    name - name of the document (for printing purposes)
    Return - nothing'''
    high_count = 20
    low_count = 2
    body = ''
    for word,cnt in nameTuple:
        body = body + " " + make_HTML_word(word, cnt,high_count,low_count)
    #print(body)
    box = make_HTML_box(body)
    #print(box)
    print_HTML_file(box, name)



transcriptFile = input("Enter the transcript file to be processed: ")
stopWords = readStop('WordsToIgnore.txt')

documentList = readDocument(stopWords, transcriptFile)

wordCount = countWords(documentList)

wordCountToTuple = countToTuples(wordCount)

wordCountToTuple.sort(reverse=True)

printFrequency(wordCountToTuple[:40], 'Output')

documentTop40 = [(t[1],t[0]) for t in wordCountToTuple[:40]]
documentTop40.sort()

makeBoxHTML(documentTop40, 'Output')
