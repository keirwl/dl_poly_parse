#!/usr/bin/env python

# dl_poly_parse
# If ran as script, takes a DL_POLY OUTPUT file and returns the physical properties as a parsed
# file of simple columns, for easy readability by plotting software.
#
# To do:
#  * give option to output as csv
#  * give option to return properties as horizontally or vertically sorted
#  * allow importing as library to get single properties as lists

def getLines(OUTPUT):
	with open(OUTPUT, "r") as f:
		lines = f.readlines()
	return lines

def getHeaders(OUTPUT, BREAK):
	lines = getLines(OUTPUT)
	firstBreak = lines.index(BREAK)
	headers = lines[firstBreak+2].split() + lines[firstBreak+3].split() + lines[firstBreak+4].split()
	headers.remove("(s)")
	headers[headers.index("cpu")] = "cpu (s)"
	return headers


def getProperty(OUTPUT, property):
	pass

def sortList(unsorted):
	# returns list reading down each column of 3 in OUTPUT rather than across each row
	# this puts certain values usefully adjacent to each other e.g. time, step, cpu
	# but separates others e.g. alpha, beta, gamma
	sort = []
	for i in range(0,len(unsorted)):
		triple = unsorted[i::10]
		for j in triple:
			sort.append(j)
	return sort[:30]

def getAllProps(OUTPUT, BREAK):
	# returns physical properties as a huge list of lists

	lines = getLines(OUTPUT)
	headers = getHeaders(OUTPUT, BREAK)
	properties = []

	for i, l in enumerate(lines):
		if l == BREAK and len(lines[i+1].split()) == 10: # data always found in lines of 10 after BREAK
			values = lines[i+1].split() + lines[i+2].split() + lines[i+3].split()
			
			if properties == []:	# fill with lists of initial values if empty
				properties = [[v] for v in values]
			else: 					# append otherwise
				for j, p in enumerate(properties):
					p.append(values[j])

	return len(properties[0]), headers, properties
		# could optimise by initialising each list with zeroes

def main():
	OUTPUT = "OUTPUT"
	PARSED = "PARSED"
	BREAK = " ------------------------------------------------------------------------------------------------------------------------\n"

	n, headers, properties = getAllProps(OUTPUT, BREAK)
	sortedHeaders = sortList(headers)
	sortedProps = sortList(properties)

	parsed = ""
	for h in sortedHeaders:
		parsed += "%-12s" % (h)
	for i in range(0,n):
		parsed += "\n"
		for p in sortedProps:
			parsed += "%-11s " % (p[i])


	with open("PARSED", "w") as f:
		f.write(parsed)

if __name__ == '__main__':
	main()