#!/usr/bin/python

import sys
import json
import string

args = sys.argv
num = len(args)

if num != 3:
	print "input must be as follows:"
	print "python thou.py [shakespeare.txt] [not.txt]"

file1 = open(args[1], 'r')
file0 = open(args[2], 'r')
stop = open('stopwords.txt', 'r')
punc = open('punctuation.txt', 'r')

d_stop = {}
for line in stop:
	word = line.rstrip()
	#print word
	if d_stop.has_key(word):
		continue
	d_stop[word] = 1

d_punc = {}
for line in punc:
	p = line.rstrip()
	if d_punc.has_key(p):
		continue
	d_punc[p] = 1

def clean_word(word):
	word = word.lower()
	for x in d_punc:
		word = word.replace(x,"")
	word = word.replace("\t","")
	word = word.replace("\n","")
	word = word.replace("\r","")
	word = filter(lambda x: x in string.printable, word)
	return word

all_words = []
all_lines = []

def line_count(line):
	count = 0
	for x in line:
		if x == ' ':
			count += 1
	return count

def get_counts(f, val):
	d = {}
	for line in f:
		strip = " ".join(line.split())
		if strip == "":
			continue
		#print strip
		words = line.split(" ")
		clean_line = ""
		for x in words:
			x = clean_word(x)
			if d_stop.has_key(x) or x == "":
				continue
			if d.has_key(x):
				d[x] = d[x] + 1
			else:
				all_words.append(x)
				d[x] = 1
			clean_line += x + " "
		if line_count(clean_line) < 5:
			continue
		clean_line = clean_line.rstrip()
		all_lines.append(clean_line + ":" + str(val))
	sorted_d = sorted(d.items(), key=lambda x: x[1])
	return d

d1 = get_counts(file1, 1)
d0 = get_counts(file0, 0)
all_words = sorted(all_words)

def to_file(arr, f):
	fout = open(f,'w')
	for x in arr:
		fout.write(x + "\n")
	fout.close()

to_file(all_words, "words.txt")
to_file(all_lines, "lines.txt")

count_grid = {}

for word in all_words:
	y1x1 = 0
	if d1.has_key(word):
		y1x1 = d1[word]
	y1x0 = len(d1) - y1x1
	y0x1 = 0
	if d0.has_key(word):
		y0x1 = d0[word]
	y0x0 = len(d0) - y0x1
	total = y1x1 + y1x0 + y0x1 + y0x0
	grid = [[y1x1 * 1.0 / total, y1x0 * 1.0 / total], [y0x1 * 1.0 / total, y0x0 * 1.0 / total]]
	count_grid[word] = grid

fjson = open('prob.json','w')
fjson.write(json.dumps(count_grid, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=True))
fjson.close()


