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
# TODO: This currently doesn't handle commands in other commands.
# And it doesn't handle multiple commands on the same line.
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
    # We need to go down to the character level.
    if openWrapper in string and closeWrapper in string:
        curlyContent = string[string.index(openWrapper)+1:string.index(closeWrapper)]
        return(curlyContent)
    # Else, return the string.
    else: 
        identity = ''
        return(identity)

def curlyTwo(string, wo='{', wc='}'):
    n = 0
    j = 0
    k = 0
    d = [] 
    l = []
    splat = [c for c in string]
    for i in range(len(splat)):
        if splat[i] == wo:
            n+=1
            d.append([n,'o',i])
        elif splat[i] == wc:
            d.append([n,'c',i]) 
            n-=1
    print(d)
    while j < len(d):
        if d[j][0] == d[j+1][0] and d[j][1]=='o' and d[j+1][1]=='c':
            l.append([d[j][2],d[j+1][2]])
            d.remove(d[j+1]) # this has to come first, otherwise, you end up trying
            # to get the second element of a singleton list
            d.remove(d[j]) 
        j+=1 
    while k < len(d):
        print(k)
        l.append([d[0][2],d[-1][2]])
        d.remove(d[-1])
        d.remove(d[0])
        k+=1
    print(d)
    return(l)

test = "\\textbf{sdf}"
test2 = "\\textbf{it\\textit{al}ic}"
test3 = "\\textbf{test}\\testit{adsf}"
test4 = "\\textbf{test}\\testit{\textbf{\textit{adsf}}adsf}\textit{adsf}"

print(curlyTwo(test4))

# This will take a tag (e.g., b) and some content, and output that content in
# those tags (e.g., makeTag("i","test") returns "<i>test</i>")
def makeTag(tag,content):
    return("<"+tag+">"+content+"</"+tag+">")

# Translate latex typesetting commands into HTML tags. Uses a dictionary.
# Currently, this doesn't return lines it returns just the tag.
def texToTag(ligne):
    texDict = {
            "\\textbf": "b",
            "\\textit": "i",
            "\\section": "h2",
            "\\section*": "h2",
            "\\emph": "i"
            }
    for key in texDict.keys():
        if key in ligne:
            return(makeTag(texDict[key], curlyGrab(ligne)))

def translate(liste):
    tempList = []
    for i in range(len(liste)): 
        # print(texToTag(liste[i]))
        tempList.append(texToTag(liste[i])) 
    return(tempList)



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

def newLine(liste):
    tempList = []
    for i in range(len(liste)):
        tempList.append(liste[i]+"<br>\n")
    return(tempList)

def noPreamble(liste):
    tempList = []
    beg = 0
    end = 0
    for i in range(len(liste)):
        if "maketitle" in liste[i]: 
            beg = i
        elif "end{document}" in liste[i]:
            end = i
    tempList = liste[beg+1:end]
    return(tempList)

def cleanMyInput(liste):
    tl = []
    tl = noComment(liste)
    tl = noPreamble(tl)
    tl = noWhitespace(tl)
    tl = newLine(tl)
    return(tl)

#texPlay=cleanMyInput(texPlay)


for i in range(nbegdoc): 
    if "\\title" in texcontent[i]:
        title = curlyGrab(texcontent[i])
    if "\\author" in texcontent[i]:
        author = curlyGrab(texcontent[i])


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

