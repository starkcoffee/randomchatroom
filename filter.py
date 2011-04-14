import re
import cgi
import Cookie
import logging

swearList = None

#Deletes strings that are too long.
def length(string):
    split = string.split(" ")
    string = ""
    for s in split:
    	if len(s) < 120:
    		split[split.index(s)] = []
    		string = string + s + " "
    string = string.strip()
    return string
    
def getSwears():
    global swearList
    if swearList != None:
        return swearList
    else:
        logging.info("loading swearList")
        file = open("filter","r")
        swearList = file.readlines()
        file.close()
        return swearList
        
#Deletes swears
def swears(string):
    rudishWords = getSwears()
    for word in rudishWords:
        pattern = re.compile(word,re.IGNORECASE | re.VERBOSE)
        string = re.sub(pattern,'banana',string)
    return string

#@Name Matching, because I could and it was suggested. =3
def twitter(string,name):
    pattern = "\A@(\w+)"
    search = re.search(pattern,string)
    if search:
        find = re.compile(search.group(1),re.I)
        if re.search(find,name):
            string = re.sub(find,"<blink><font color='red'>@"+ name +"</font></blink>",string)[1:]
    return string

#Deletes swears and highlights links
def html(string, extra=""):
    string = cgi.escape(string)

    ####       TAG REPLACEMENT METHOD       ####

    ##goodHTML = ["a",
    ##            "b",
    ##            "i",
    ##            "s",
    ##            "u",
    ##            "big",
    ##            "bdo",
    ##            "del",
    ##            "sub",
    ##            "sup",
    ##            "font",
    ##            "blink",
    ##            "color"]
    ##split = re.split("[>|<]",string)
    ##
    ##if len(split) > 1:
    ##    tags = split[:]
    ##    text = split[:]
    ##    loopCnt = 0
    ##    newtags = split[:] #Clearing this.
    ##    for s in split:
    ##        newtags[loopCnt]=""
    ##        tag = s.strip()
    ##        if tag != "": #Filter out blanks found through split
    ##            if loopCnt % 2 == 0:
    ##                tags[loopCnt] = ""
    ##                text[loopCnt] = s + " " #Adding to get the URL clearer after.
    ##            else:
    ##                text[loopCnt] = ""
    ##                tags[loopCnt] = s + " "
    ##        loopCnt += 1
    ##    for s in goodHTML:
    ##        pattern = re.compile(s,re.I)
    ##        for tag in tags:
    ##            print s
    ##            if tag == "": continue
    ##            closeTag = tag.split(" ")[0]
    ##            if tag[0] != "/" and tags.count("/"+closeTag) == 0: tags.append("/"+closeTag)
    ##            if not re.search(pattern,tag):
    ##                newtags[tags.index(tag)] = s
    ##
    ##    string = ""
    ##    loopCnt = 0
    ##    print tags
    ##    for s in text:
    ##        if text[loopCnt] != "":
    ##            string = string + text[loopCnt]
    ##            print text[loopCnt]
    ##        elif tags[loopCnt] != "":
    ##            string = string + '<' + tags[loopCnt] + '>'
    ##            print tags[loopCnt]
    ##        loopCnt += 1
    ##else: text = string
    
    #IMG showing (Shh, it's a secret to all the foreigners. =3)
    pattern = re.compile("img:(\S+)",re.I)
    search = re.search(pattern,string)
    # if search:
    	# url = search.group(1)
    	# if re.search("https://",url):
    		# code = "<img src='" + url + "' alt='Image' />"
    	# else:
    		# url = re.sub("http://","",url)
    		# code = "<img src='http://" + url + "' alt='Image' />"
    	# string = re.sub(pattern, code, string)
    # else:
    #URL matching
    pattern = "((?:(?:http[s]?://)|(?:www.))(?:\S+))[\w]"
    search = re.search(pattern,string)
    if search:
        logging.info("DERP")
        for search in re.finditer(pattern, string):
         url = search.group(0)
         if search.group(1) != None:
            if re.search("https://",url):
                url = "https://"+re.sub("https://","",url)
                code = "<a href='" + url + "'>"+url+"</a>"
            else:
                url = re.sub("http://","",url)
                code = "<a href='http://" + url + "'>"+url+"</a>"
            string = re.sub("(?:http[s]?://)?"+url, code, string)
    return string
    
def all(string,extra=""):
    string = swears(string)
    string = length(string)
    string = html(string,extra)
    return string
