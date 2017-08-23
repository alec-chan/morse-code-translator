#!/usr/bin/env python
import sys
import re
import math
import struct
import pyaudio
import time
import imp
#morse code hash table, morse encoding is the key and chars are values
morse_dict = {'.-':'A',
		 '-...':'B',
	 	 '-.-.':'C',
 	 	 '-..':'D',
 	 	 '.':'E',
 	 	 '..-.':'F',
 	 	 '--.':'G',
 	 	 '....':'H',
 	 	 '..':'I',
 	 	 '.---':'J',
 	 	 '-.-':'K',
 	 	 '.-..':'L',
 	 	 '--':'M',
 	 	 '-.':'N',
 	 	 '---':'O',
 	 	 '.--.':'P',
 	 	 '--.-':'Q',
 	 	 '.-.':'R',
 	 	 '...':'S',
 	 	 '-':'T',
 	 	 '..-':'U',
 	 	 '...-':'V',
 	 	 '.--':'W',
 	 	 '-..-':'X',
 	 	 '-.--':'Y',
 	 	 '--..':'Z',
 	 	 '.-.-.-':'.',
 	 	 '--..--':',',
 	 	 '..--..':'?',
 	 	 '-..-.':'/',
 	 	 '.--.-.':'@',
 	 	 '.----':'1',
 	 	 '..---':'2',
 	 	 '...--':'3',
 	 	 '....-':'4',
 	 	 '.....':'5',
 	 	 '-....':'6',
 	 	 '--...':'7',
 	 	 '---..':'8',
 	 	 '----.':'9',
 	 	 '-----':'0',
 	 	 '/':' '}


###################
# Audio Functions #
###################

def play_tone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / fs
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in xrange(N))
    # todo: get the format from the stream; this assumes Float32
    data = ''.join(struct.pack('f', samp) for samp in tone)
    for n in xrange(T):
        stream.write(data)



def play_dit(p, fs, stream):
	play_tone(800, 0.5, 0.125, fs, stream)


def play_dah(p, fs, stream):
	play_tone(800, 0.5, 0.375, fs, stream)

###################

#translate from morse to text
def morse_to_text(morse):

	s=""
	for char in morse.split():
		if char not in morse:
			print "Invalid morse code, "+char
			break
		else:
			s+=morse_dict[char]
	
	print morse+" -> "+s
	
	

#translate from text to morse
def text_to_morse(text):
	fs = 48000
	p = pyaudio.PyAudio()
	stream = p.open(
    	format=pyaudio.paFloat32,
    	channels=1,
    	rate=fs,
    	output=True)
	s=""
	for char in text:
		s+=morse_dict.keys()[morse_dict.values().index(char)]
		s+=" "
	print text+" -> "+s
	for c in s.replace(" ",""):
		if c=="-":
			play_dah(p, fs, stream)
			time.sleep(0.2)
		if c==".":
			play_dit(p, fs, stream)
			time.sleep(0.2)
		if c=="/":
			time.sleep(0.8)
	stream.close()
	p.terminate()


#input parser
def parse_input(text=""):
	try:
		if text=="":
			text=str(raw_input('Enter some text:'))
		else:
			text=str(text)

		if re.search('[a-zA-Z]', text):
			text.upper()
			text_to_morse(text)
		else:
			morse_to_text(text)

	except ValueError:
		print "Not a string"

#checks if the pyaudio module is installed
def check_pyaudio():
	try:
		imp.find_module('pyaudio')
		return True
	except ImportError:
		print "Pyaudio is not installed; try 'pip install pyaudio' or visit: http://people.csail.mit.edu/hubert/pyaudio/"
    	return False

#main
if __name__ == "__main__":

	if check_pyaudio():
		if len(sys.argv)>1:
			parse_input(sys.argv[1])
		else:
			print ""
			print "International Morse Code Translator"
			parse_input()
	else:
		sys.exit(1)



