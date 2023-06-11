#!/usr/bin/python3
from OSC import *

import sys
import time
import traceback

c = OSCStreamingClient()

##### THIS IS WHERE WE CONNECT TO EOS
c.connect(('127.0.0.1', 3032))
#c.connect(('10.101.93.101', 3032))

def eos_out_handler(addr, tags, stuff, source):
	1	
c.addMsgHandler('default', eos_out_handler)

#read file to get the list of names

if len(sys.argv) != 2 :
	print('Invalid number of arguments. Usage: fixmyshow.py filename.csv')
	exit(1)	
f = open(sys.argv[1], 'r')
try:

	with open(sys.argv[1], 'r', encoding='utf-8-sig') as f:
		for line in f:
			res = line.split(',')
			list_num = res[0].strip()
			if len(res) > 1 :
				act_name = res[1].strip()
			if len(res) > 2 :
				act_desc = res[2].strip()
			if len(res) > 3 :
				start_notes = res[3].strip()
			if len(res) > 4 :
				ending_notes = res[4].strip()
			print("{} {} ({}) START {} END {}".format(list_num, act_name, act_desc, start_notes, ending_notes)) 
			c.sendOSC(OSCMessage("/eos/newcmd", "Cue 99 /  Copy_To Cue {} / Enter".format(list_num)))
			c.sendOSC(OSCMessage("/eos/set/cuelist/{}/label".format(list_num), "{} ({})".format(act_name, act_desc)))	

			if start_notes:
				c.sendOSC(OSCMessage("/eos/set/cue/{}/0.5/label".format(list_num), start_notes))
			if ending_notes:
				c.sendOSC(OSCMessage("/eos/set/cue/{}/100/label".format(list_num), ending_notes))
		time.sleep(1)
		c.close()	
		sys.exit()

except Exception as e:
	traceback.print_exc()
	print(str(e))
	c.close()

