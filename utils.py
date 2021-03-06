import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, re

def ParseArgs (str, num):
	str = str.strip ()
	str = str.replace ('\\"', '\x000')

	if len(str) == 0:
		return None
	
	if num == 1:
		return [str]
	
	parts = str.split (' ')
	newParts = []
	
	tmpArg = None
	for i in range (0, len (parts)):
		p = parts[i]
		
		if not tmpArg is None: # jeli cos juz sklejamy
			if len (p) == 0:
				tmpArg += " "
			elif p[-1] == '"':
				tmpArg += " " + p[:-1]
				newParts.append (tmpArg)
				tmpArg = None
			else:
				tmpArg += " " + p
		else:
			if len (p) == 0:
				newParts.append (" ")
			elif len (p) > 1 and p[0] == '"' and p[-1] == '"': # jesli "Abc" ale nie ""
				newParts.append (p[1:-1])
			elif p[0] == '"':
				tmpArg = p[1:]
			else:
				newParts.append (p)
	
		if num != -1 and len (newParts) == num - 1:
			break
	
	# print("1 pass")
	# print(newParts)
	
	for j in range (0, len (newParts)):
		newParts[j] = newParts[j].replace ('\x000', '"')
	
	# print(i)
	if i + 1 < len(parts):
		tmp = " ".join (parts[i + 1:])
		tmp = tmp.replace ('\x000', '\\"')
		newParts.append (tmp)
		
	# print("2 pass")
	# print(newParts)
	
	if len (newParts) < num:
		return None
	
	return newParts

def GetShortLink (url):
	try:
		return urllib.request.urlopen ("http://tinyurl.com/api-create.php?url=" + urllib.parse.quote_plus (url)).read ()
	except:
		return url

def noHL(text):
	mid = int(len(text) / 2)
	return text[0:mid] + "\u200b" + text[mid:]

def nickBasename(nick):
	# print (nick)
	parts = re.split("\|", nick)
	nick = parts[0]
	nick = re.sub("\d+$", "", nick)
	# print (nick)
	return nick
