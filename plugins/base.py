# coding=utf-8
from ext import *
import datetime, re, time, select, random, os, json, time, urllib2
from subprocess import *
import utils

@command ("help", -1)
def c (ircbot, args):

	if args:
		for plugin in pm.commands:
			if plugin["type"] == 0 and plugin["name"] == args[0]:
				if "desc" in plugin:
					ircbot.Reply ("*" + plugin["name"] + "*: " + plugin["desc"])
				else:
					ircbot.Reply ("*" + plugin["name"] + "*: no description")
				return
	
	str = []	
	for plugin in pm.commands:
		if plugin["type"] == 0:
			str.append (plugin["prompt"] + plugin["name"])
	str = ", ".join (str)

	ircbot.Reply (str)

@command ("mute", 1)
def c (ircbot, args):
	if not ircbot.GetLastSenderObj () or not ircbot.GetLastSenderObj ().op:
		return
	
	if args[0] == "1":
		ircbot.mute = True
		ircbot.Reply ("muted")
	elif args[0] == "0":
		ircbot.mute = False
		ircbot.Reply ("unmuted")
		
@command ("g", 1)
@desc ("gugiel")
@usage ("!g fraza")
def c (ircbot, args):
	if ircbot.mute: return
	ircbot.Reply ("http://google.pl/search?q="+args[0].replace (" ", "+"))

@command ("args", 2)
@usage ("!args num arg0 arg1...")
def c (ircbot, args):
	if ircbot.mute: return
	ircbot.Reply (str(utils.ParseArgs (args[1], int(args[0]))))
	
@command ("paste", 0)
@desc ("2 pasty")
def c (ircbot, args):
	if ircbot.mute: return
	ircbot.Reply ("http://pastebin.com http://pastebin.pl")
	
@command ("data", 0)
@desc ("data?")
def c (ircbot, args):
	if ircbot.mute: return
	ircbot.Reply (str(datetime.datetime.now ()))
	
@command ("rand", 0)
@desc (u"Zwraca losową liczbę z zakresu 1-6")
def c (ircbot, args):
	if ircbot.mute: return
	ircbot.Reply ("4")
	
@command ("rrs", 0)
def c (ircbot, args):
	global rr1, rr2
	
	#if rr1 != 0 and rr2 != 0:
	#	ircbot.Reply (";> .. the last one first ;>")
	#	return
	
	rr2 = random.randint (2, 10)
	rr1 = random.randint (1, rr2 - 1)
	ircbot.Reply ("done! ({0} .. {1})".format (rr1, rr2))
	
	#return
	
	#try:
	#	_rr1 = int(args[0])
	#	_rr2 = int(args[1])
	#except ValueError:
	#	ircbot.Reply ("fakaf!")
	#	return
	#if _rr1 > 10 or _rr2 > 10 or _rr1 < 1 or _rr2 < 1 or _rr1 > _rr2:
	#	ircbot.Reply ("fakaf!")
	#	return
	#rr1 = _rr1
	#rr2 = _rr2
	#ircbot.Reply ("done!")

rr1 = rr2 = 0
@command ("rr", 0)
def c (ircbot, args):
	global rr1, rr2
	
	if rr1 == 0 or rr2 == 0:
		ircbot.Reply ("empty!")
		return
	
	s = ircbot.GetLastSender ()
	if rr1 == rr2 or random.randint (1, rr2) <= rr1:
		rr1 = rr1 - 1
		rr2 = rr2 - 1
		ircbot.Reply ("chlip " + random.choice ([":D", ":/", "/:|", ";p", "<3", "3<"]))
		ircbot.Kick ("stosowana", s, "by rr")
	else:
		rr2 = rr2 - 1
	ircbot.Reply ("... ({0} .. {1})".format (rr1, rr2))

@prompt (".")
@command ("lod", -1)
def c (ircbot, args):
	if ircbot.mute: return
	if ircbot.GetUserByNick ("Olivia") == None:
		if args is None or len(args) == 0:
			ircbot.Reply (ircbot.GetLastSender () + u": ಠ_ಠ")
		else:
			ircbot.Reply (" ".join (args) + u": ಠ_ಠ")

bch = None

"""
@command ("c", 1)
def c (ircbot, args):
	if ircbot.mute: return
	p = Popen (["/usr/bin/bc", "-l"], stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=0)
	p.stdin.write (args[0] + "\n")
	p.stdin.close ()
	out = ""
	err = ""

	lastRead = time.time ()
	while time.time () - lastRead < 0.5:
		p.poll ()
		print "ret:", p.returncode
		if p.returncode == 0:
			break
		
		q = select.select ([p.stdout, p.stderr], [], [], 0.1)
		if p.stdout in q[0]:
			out += p.stdout.read (1)
			lastRead = time.time ()
			print "out:", out
		if p.stderr in q[0]:
			err += p.stderr.read (1)
			lastRead = time.time ()
			print "err:", err

	p.poll ()
	if p.returncode == None:
		print "kill"
		res = "timeout!"		
		if len(err) > 0:
			res += " (err: {0})".format (err)
		p.kill ()
	else:
		res = out
		if len(err) > 0:
			res = "!!! (err: {0})".format (err)
	
	ircbot.SendChannelMessage ("#stosowana", res)
"""

lastNick = None
lastNick2 = None
lastDMessage = ""

@command ("makefun", 0)
def c (ircbot, args):
	global lastDMessage
	lastDMessage = ""

@command ("reverse", 1)
def c (ircbot, args):
	ircbot.Reply (args[0][::-1])
	
@handler ("message_public")
def c (ircbot, sender, message):
	global lastNick, lastNick2, lastDMessage
	lastNick2 = lastNick
	lastNick = sender
	
	if ircbot.mute: return
	if sender == "kdbot":
		return
	if sender == "Kajtek":
		message = message.strip ()
	nofun = False
	for c in message:
		if c != '.':
			nofun = True
		
	if not nofun:
		if len(message) != len(lastDMessage) + 1:
			ircbot.Kick ("stosowana", sender, ":D")
		else:
			lastDMessage = message

@command ("slap", 0)
def c (ircbot, args):
	if ircbot.mute: return
	global lastNick2
	if lastNick2 != None:
		msg = "slaps " + lastNick2
		ircbot.SendChannelMessage ("#stosowana", "\x01ACTION {0}\x01".format (msg))

@command ("madzia", 0)
def c (ircbot, args):
	if ircbot.mute: return
	data = [
		u"Jakie przyjemne są te zajęcia, zawsze widzę stąd kopiec Kościuszki, lubię tę salę...",
		u"No i tutaj pan sobie zastosuje jakieś tam prawa, już nie pamiętam jak się nazywały...",
		u"I tutaj mamy jeden bit na bit.",
		u"Obecne karty graficzne mają tysiące albo miliony rdzeni.",
		u"Niech pan wybierze sobie dowolną liczbę 7.",
		u"Co się uciecze to nie utonie.",
		u"i proszę mi tutaj sztachetek nie rysować!",
		u"nanomilimetry",
		u"To jest trochę \"inna\" informatyka.",
		u"Samolot bening.",
		u"Ja panu nie włożę tego wzoru do głowy szufladą.",
		u"W Pixarze renderowanie filmow zajmuje miliony godzin.",
		u"Czas wykonania operacji zmiennoprzecinkowej na karcie graficznej wynosi 50% czasu wykonania operacji zmiennoprzecinkowej na tej karcie.",
		u"To panowie są braciami?",
		u"\"W madziolotku nie zmieniają się pytania, zmieniają się odpowiedzi.\"",
		u"Ile może mieć słowo bitów?? no może mieć np 32,64,121, dobrze mówię?",
		u"Tekturowy świat? Chyba powinien być cyfrowy",
		u"O jaki brzydki, taki brzydki kwadrat, toczony jakiś!",
		u"A co pan tu rysujesz, aaaaaaaaa, chciał Pan ładnie to zrobić.",
		u"Pan siedzi jakby Pan był..., a nie, nie będę złośliwa.",
		u"Ja nie prowadzę wykładu żeby sama ze sobą rozmawiać, bo ja sobie z każdym rokiem coraz lepiej to wszystko utrwalam!",
		u"Chińczycy są na tyle sprytni że niedługo przetłumaczą nasz język i ZJEDZĄ NAS",
  ]
	
	ircbot.Reply (u"{0}: {1}".format (ircbot.GetLastSender (), random.choice (data)))

@command ("gurgul", 0)
def c (ircbot, args):
	if ircbot.mute: return
	data = [u"mówi", u"słyszy", u"dzwoni", u"widzi", u"wie", u"dosięgnie", u"ogarnia", u"pomoże"]
	ircbot.Reply (u"{0}: {1}".format (ircbot.GetLastSender (), random.choice (["Bubargul ", "Gurgul "]) + random.choice (data)))

@command ("board", 0)
def c (ircbot, args):
	if ircbot.mute: return
	ircbot.Reply ("http://cosketch.com")

last = -1
@command ("last", 0)
@desc ("Time elapsed since previous call")
def c (ircbot, args):
	global last
	if ircbot.mute: return
	if last != -1:
		ircbot.Reply (str(time.time () - last))
	last = time.time ()

@command ("say", 1)
def c (ircbot, args):
	if ircbot.mute: return
	if ircbot.GetLastSender ():
		if ircbot.GetLastSender () == "koziolek":
			ircbot.Reply ("koziolek: you're so.. so..., no, I won't be malicious.")
		else:
			ircbot.Reply (ircbot.GetLastSender () + " forced me to say: " + args[0])

@command ("lisp", 0)
def c (ircbot, args):
	s = ""
	for i in xrange (50):
		s += random.choice ("()")
	ircbot.Reply ("(" + s + ")")

@command ("temp", 0)
def c (ircbot, args):
	ircbot.Reply (urllib2.urlopen ("http://83.175.189.46:3434/outtemp.php").read () + u"°C");
