#!/usr/bin/python3
from OSC import *

import sys
import time

c = OSCStreamingClient()

##### THIS IS WHERE WE CONNECT TO EOS
c.connect(('127.0.0.1', 3032))
#c.connect(('10.101.93.101', 3032))

def eos_out_handler(addr, tags, stuff, source):
	1	
c.addMsgHandler('default', eos_out_handler)

#read file to get the list of names

if len(sys.argv) != 3 :
	print('Invalid number of arguments. Usage: fixmyshow.py filename_source.tsv filename_order.tsv')
	exit(1)	
songs = dict()
try:
	with open(sys.argv[1], 'r', encoding='utf-8-sig') as f:
		for line in f:
			res = line.split(',')
			list_num = res[0].strip()
			act_name = res[1].strip().upper()
			act_desc = res[2].strip()
			#print("{} {} ({})".format(list_num, act_name, act_desc)) 
			songs[act_name] = list_num
			# c.sendOSC(OSCMessage("/eos/set/cuelist/{}/label".format(list_num), "{} ({})".format(act_name, act_desc)))	
		time.sleep(1)
except:
	c.close()
	sys.exit()

#print(songs)

try :
	with open(sys.argv[2], 'r', encoding='utf-8-sig') as f:
		previous = -1
		for line in f:
			if previous == -1 :
				print("START")
			res = line.split(',')
			incoming_act = res[1].strip()
			#print(incoming_act)
			if not incoming_act.upper() in songs :
				print("SKIPPING {}".format(incoming_act))
				continue
			incoming_num = songs[incoming_act.upper()]
			print("{}: Act {} list {} previous {}".format(res[0], incoming_act, incoming_num, previous)) 
			if not previous == -1:
				c.sendOSC(OSCMessage("/eos/newcmd", "Cue {} / 100  Link Cue {} / Enter".format(previous, incoming_num)))
			previous = songs[incoming_act.upper()]
	time.sleep(1)
	c.close()
except Exception as e: 
	print("EXCEPTION")
	print(e)
	time.sleep(1)
	c.close()
	sys.exit()

sys.exit()
