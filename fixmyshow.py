#!/usr/bin/python3
from OSC import *

import sys
import time
import traceback
import csv

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

		header_dance_name = 'Name of Dance'
		header_q_list = 'LX Cue List Number'
		header_dance_style = 'Dance Style'
		header_age_range = 'Age Range'
		header_start_notes = 'Dance Beginning Info'
		header_end_notes = 'Dance End Info'

		csv = csv.DictReader(f)
		# print(csv)

		for line in csv :
			# print(line)
			if(line[header_q_list] == ''):
				print("Skipping list without cue list number {}".format(line[header_dance_name]))
				continue
			if int(line[header_q_list]) > 990:
				print("Skipping utility list {} {}".format(
					line[header_q_list], line[header_dance_name], line[header_dance_style]))
				continue
			print("{} {} ({} - {}) START {} END {}".format(line[header_q_list], line[header_dance_name], line[header_dance_style], line[header_age_range], line[header_start_notes], line[header_end_notes]))

			c.sendOSC(OSCMessage(
				"/eos/newcmd", "Cue 99 /  Copy_To Cue {} / Enter".format(line[header_q_list])))
			c.sendOSC(OSCMessage("/eos/set/cuelist/{}/label".format(
				line[header_q_list]), "{} ({} - {})".format(line[header_dance_name], line[header_dance_style], line[header_age_range])))

			if line[header_start_notes]:
				c.sendOSC(OSCMessage(
					"/eos/set/cue/{}/0.5/label".format(line[header_q_list]), line[header_start_notes]))
			if line[header_end_notes]:
				c.sendOSC(OSCMessage(
					"/eos/set/cue/{}/100/label".format(line[header_q_list]), line[header_end_notes]))
				
		c.close()	
		sys.exit()

except Exception as e:
	traceback.print_exc()
	print(str(e))
	c.close()

