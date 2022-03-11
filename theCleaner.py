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

# This function first counts opening and closing brackets and adds them to a
# list (d) with the information of whether they match (n), whether they are an
# opening or a closing bracket, and the position in the line where they occur.
# Then, it recovers the ranges that fall between two matching brackets. 
# There are two cases to consider. First, brackets that don't contain other
# brackets. Here, we pop two consecutive items from d provided that they have
# the same index n and they are respectively an opening and a closing bracket.
# The second case is one where brackets do contain other brackets. Here, we pop
# the first and the last item in d. I can't imagine any other cases.
def curlyTwo(string, wo='{', wc='}'):
    n = j = k = 0
    d = []
    l = [] 
    tmp = []
    splat = [c for c in string]
    for i in range(len(splat)):
        if splat[i] == wo:
            n+=1
            d.append([n,'o',i+1])
        elif splat[i] == wc:
            d.append([n,'c',i]) 
            n-=1
    # print(d)
    if len(d)%2 == 0: # originally, this didn't handle cases where there were no
        # matching brackets on a given line, e.g., when a bracket closes a line
        # and it's matched some lines below. To circumvent, for now, make sure
        # that the list contains an even number of elements.
        while j < len(d) - 1: # minus one here because we will never check the last
#            print(j, j+1, len(d))
            # element of the list (should always be a closing bracket).
            if d[j][0] == d[j+1][0] and d[j][1]=='o' and d[j+1][1]=='c':
                l.append([d[j][2],d[j+1][2]])
                print(d)
                d.remove(d[j+1]) # this has to come first, otherwise, you end up trying
                # to get the second element of a singleton list
                d.remove(d[j]) 
            j+=1 
        while k < len(d):
            l.append([d[0][2],d[-1][2]])
            print(d)
            d.remove(d[-1])
            d.remove(d[0])
            k+=1
        for line in l:
            tmp.append(string[line[0]:line[1]])
    else:
        tmp.append("no matching bracket")
    return(l, tmp)
# Right now, this isn't doing what it's supposed to. Cf. test7 below


# test7 = "\ref{ex:fsg1premise} \ref{ex:fsg1conclus ion} \emph{Tuesday} \emph{Peter}"# instead of on \emph{Tuesday}.  If the results of the original test and this additional test differ, then t he predicate is focus sensitive. Please refer to the  \href{https://docs.goo gle.com/document/d/1Z6OEynS_sgjbz43gjcR92ba0C1zelicaOSk9DYtCids}{predicate s pecific notes} for further details about the predicates involved and the add itional tests for them. For most predicates, it should be quite clear whethe r they are UE when the embedded clause does not contain focus, but this may not be the case for some other predicates. As a rule thumb, if you suspect t hat a predicate might be non-UE when the embedded clause does not contain fo cus, then please run the additional test just to be safe."
# test7 = "\ref{ex} \ref{to} \emph{lo}"
#test0 = "\\textbf{sdf}"
#test1 = "\\textbf{it\\textit{al}ic}"
#test2 = "\\textbf{test}\\testit{adsf}"
#test3 = "\\textbf{test}\\testit{adsf}\\textbf{asdf}"
#test4 = "\\textbf{bold}\\testsl{\\textbf{\\textit{slanted and bold and italic}}bold and slanted}\\textit{italic}"
#test5 = "\\renewcommand{\\firstrefdash}{}"
#test6 = "\newcolumntype{R}[2]{%"
#
# print(curlyTwo(test7))

# increment upon encountering ob, keep looking until you find matching cb,
# extract string, feed leftover to the same function 
# if running in a loop, you need to specify 'collect=[]' Otherwise, the list
# will just keep growing.
def curlyThree(ligne, collect=[], ob='{', cb='}'): 
    # we also need to handle the \{, \} case.
    tmp = []
    n = 0
    spligne = [char for char in ligne]
    beg = end = 0
    if ob not in spligne and cb not in spligne: # the no brackets case
        print(ligne)
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
T = [test, test2, test3]
for t in T:
    print(curlyThree(t,[])) 



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

