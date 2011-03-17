import re
import cgi
import Cookie

from google.appengine.api import memcache

def getSwears():
    words = memcache.get("rudish_words")
    if words is not None:
        return words
    else:
        file = open("filter","r")
        words = file.readlines()
        file.close()
        memcache.add("rudish_words",words,600)
        return words

def swears(string):
    rudishWords = getSwears()
    for word in rudishWords:
        pattern = re.compile(word,re.IGNORECASE | re.VERBOSE)
        string = re.sub(pattern,'banana',string)
    return string
    
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

	#@Name Matching, because I could and it was suggested. =3
	pattern = "\A@(\w+)"
	search = re.search(pattern,string)
	if search:
		find = re.compile(search.group(1),re.I)
		myName = extra
		if re.search(find,myName):
			string = re.sub(find,"<blink><font color='red'>@"+ myName +"</font></blink>",string)[1:]
	
	#IMG showing (Shh, it's a secret to all the foreigners. =3)
	pattern = re.compile("img:(\S+)",re.I)
	search = re.search(pattern,string)
	if search:
		url = search.group(1)
		if re.search("https://",url):
			code = "<img src='" + url + "' alt='Image' />"
		else:
			url = re.sub("http://","",url)
			code = "<img src='http://" + url + "' alt='Image' />"
		string = re.sub(pattern, code, string)
	else:
		#URL matching
		pattern = "((?:(?:http[s]?://)|(?:www.))(?:\S+))[\w]"
		search = re.search(pattern,string)
		if search:
			url = search.group(0)
			if search.group(1) != None:
				if re.search("https://",url):
					url = "https://"+re.sub("https://","",url)
					code = "<a href='" + url + "'>"+url+"</a>"
				else:
					url = re.sub("http://","",url)
					code = "<a href='http://" + url + "'>"+url+"</a>"
				string = re.sub(pattern, code, string)
	return string
	
def all(string,extra=""):
	string = swears(string)
	string = html(string,extra)
	return string