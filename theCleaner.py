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

# This function takes a line and a list as inputs. It appends the line to the
# list unchanged if it doesn't contain { and }. Else, it does two things.
# Encountering an opening bracket increments index n by one. Encountering a
# closing bracket decrements n by one. If n is then 0, we've encountered
# outermost brackets. Their inhalts are appended to the list 'collect'. This'll
# catch any sequence of pairs of brackets that don't contain any other brackets.
# For pairs of brackets that do contain more brackets, the inhalts first get
# appended, then we run the same function on that.
# Note: Collecting outputs in 'tmp' wasn't working (we obtained structure). So
# we collect outputs in 'collect.' It initializes as [], but it remains as is
# when the function gets called recursively. If running on a list (for x in
# list: curlyThree(x)), we have to specify curlyThree(x, []), otherwise collect
# keeps growing, keeping track of everything that has been appended before.
def curlyThree(ligne, collect=[], ob='{', cb='}'): 
    # we also need to handle the \{, \} case.
    tmp = []
    n = 0
    spligne = [char for char in ligne]
    beg = end = 0
    if ob not in spligne and cb not in spligne: # the no brackets case
        collect.append(ligne)
    else:
        for i in range(len(spligne)):
            if spligne[i] == ob:
                n += 1
                if n == 1:
                    beg = i
            if spligne[i] == cb: 
                n -= 1 
                if n == 0:
                    end = i
                    tmp.append(''.join(ligne[beg+1:end])) 
                    collect.append(''.join(ligne[beg+1:end])) 
                    #print(tmp)
        for j in range(len(tmp)):
            if ob in tmp[j] and cb in tmp[j]:
                tmp.append(curlyThree(tmp[j], collect))
    return(collect)

#nob = "testing"
test="{{1re}1{2re}2op{3eft{4n{6asdf}6}4ight}3ot{5nd}5}"
test2 = "{out{in}out}"
test3 = "{out{a{i{{}}n}a}out}"
test4 = "{s}{d}{{x}}"
#T = [test, test2, test3]
#for t in T:
#    print(curlyThree(t,[])) 
#print(curlyThree('test'))


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

#def translate(liste):
#    tempList = []
#    for i in range(len(liste)): 
#        # print(texToTag(liste[i]))
#        tempList.append(texToTag(liste[i])) 
#    return(tempList)



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
# This will handle things like a comment character ending a line.



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
    return(tl)

def translate(liste): 
    tmp = []
    for index, line in enumerate(liste):
        if "begin{itemize}" in line:
            liste[index] = "<ul>"
        elif line[0:5] == "\\item": 
            pass
            #while index < len(liste) - 1:
            #    if "\\item" in liste[index+1] and "itemize" not in liste[index+1]: 
            #        print("single line!", liste[index])
            #    elif "\\item" not in liste[index+1] and "itemize" not in liste[index+1]:
            #        print("multi line!", liste[index:index+2])
            #    break
            """
            the naive solution didn't handle items with contents on multiple
            lines. tried a bit, stopped.
            """
        elif "end{itemize}" in line:
            liste[index] = "</ul>"
    return(liste)


texPlay=cleanMyInput(texPlay)
texPlay=newLine(translate(texPlay[0:30]))


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
htmlfile.write("<div>\n<h1>"+title+"</h1>\n<h2>"+author+"</h2>\n</div>\n")
htmlfile.write("<div>\n"+' '.join(texPlay)+"\n</div>")
htmlfile.write("\n</body>\n</html>")
htmlfile.close()

