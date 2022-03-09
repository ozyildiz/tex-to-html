from git import Repo
import re
import nltk

# global variables
wd = "/home/zined/sandbox/theCleaner/src/"

##
# retrieve latest Overleaf files 
##
#giturl = " https://git.overleaf.com/61e1c8973b0cbd4c2036bea9"
#repo = Repo("questionnaire")
#o = repo.remotes.origin
#o.pull()


texfile = open(wd+"main.tex","r")
# Method read() returns a string, readlines() returns a list each of whose
# elements is a line, readline() returns a string consisting of a single line.
# Every time read is run, the pointer (?) advances one step forward. Simple read
# and realines take you to the end of the file, readline takes you to the next
# line.
texcontent = texfile.readlines()
texfile.close()


# Index of "\begin(document)"
nbegdoc = texcontent.index("\\begin{document}\n")
# Mess around with texPlay rather than texcontent
texPlay = texcontent

# Function curlyGrab looks at a string and returns its substring contained in
# (by default:) curly brackets if there is one. Can handle parentheses and
# square brackets.
def curlyGrab(string, Wrapper='{'): 
    # We could use a dictionary, but they're not symmetric so it won't simplify
    # things?
    opens = ['{', '(', '[']     # opening parens
    closes = ['}', ')', ']']    # closing parens
    # If left paren is argument, use it and find matching right paren.
    # Same for if right paren is argument.
    if Wrapper in opens:        
        openWrapper = Wrapper
        closeWrapper = closes[opens.index(Wrapper)] 
    elif Wrapper in closes:    
        closeWrapper = Wrapper
        openWrapper = opens[closes.index(Wrapper)]
    # If there is a substring enclosed in argument parens, return that substring
    if openWrapper in string and closeWrapper in string:
        curlyContent = string[string.index(openWrapper)+1:string.index(closeWrapper)]
        return(curlyContent)
    # Else, return the string.
    else: 
        identity = string
        return(identity)


# This will take a tag (e.g., b) and some content, and output that content in
# those tags (e.g., makeTag("i","test") returns "<i>test</i>")
def makeTag(tag,content):
    return("<"+tag+">"+content+"</"+tag+">")

# Translate latex typesetting commands into HTML tags.
# We might want to use a dictionary 
def texToTag(liste):
    texDict = {
            "\\textbf": "b",
            "\\textit": "i",
            "\\section": "h2",
            "\\section*": "h2",
            "\\emph": "i"
            }
    for key in texDict.keys():
        if key in liste:
            return(makeTag(texDict[key], curlyGrab(liste)))

# print(texToTag("\\section*{test}"))

# Turn itemize and enumerate into lists.

####
# WE WILL HAVE CLEANING FUNCTIONS THAT REMOVE THINGS LIKE WHITESPACE THAT HTML
# CAN'T SEE. THEN WE WILL HAVE FUNCTIONS THAT ADD IN HTML. 
####

# This function should get rid of anything that follows the first '%' character
# in a line. The if statement says to collect lines that don't have '%' in
# them as is. The elif statement splits each line into a list of characters and
# retrieves the index of the first '%'. It then collects the line up to that
# index. We need to go to the level of the character because some comments start
# like this "% Comment" and some start like this "%Comment". Using split() on
# the line treats these differently: ['%', 'Comment'] vs. ['%Comment'], and the
# '%' character in the second case becomes invisible.
def noComment(liste):
    tempList = []
    for i in range(len(liste)):
        if '%' not in liste[i]:
            tempList.append(liste[i])
        elif '%' in liste[i]:
            indexOfPercent = [char for char in liste[i]].index('%')
            tempList.append(liste[i][:indexOfPercent])
    return(tempList)


# This gets rid of all \n and \ts, as well as leading and trailing whitespace.
# The split() method returns a list of words that excludes whitespace characters.
# ' '.join() joins that list putting a space in between.
def noWhitespace(liste):
    tempList=[]
    for i in range(len(liste)):
        if liste[i].split() != []:
            tempList.append(' '.join(liste[i].split()))
    return(tempList)


def cleanMyInput(liste):
    return(noWhitespace(noComment(liste)))


def newLine(liste):
    tempList = []
    for i in range(len(liste)):
        tempList.append(liste[i]+"<br>\n")
    return(tempList)

for i in range(nbegdoc): 
    if "\\title" in texcontent[i]:
        title = curlyGrab(texcontent[i])
    if "\\author" in texcontent[i]:
        author = curlyGrab(texcontent[i])

texPlay=newLine(cleanMyInput(texPlay))

##
# Grab title and author
# The for loop ranges over lines that precede begin{document}, if the string
# "title" is in that line, we extract whatever is between curly brackets in that
# line. Same for author.
##

# There's going to be a better way of doing the following
htmlfile = open(wd+"index.html","w+")
htmlfile.write("<html>\n<head>\n</head>\n<body style='color: gray; background-color: black;'>\n")
htmlfile.write("<div>\n<h1>"+title+"</h1>\n<h2>"+author+"<h2>\n</div>\n")
htmlfile.write("<div>\n"+' '.join(texPlay)+"\n</div>")
htmlfile.write("\n</body>\n</html>")
htmlfile.close()

