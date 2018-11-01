import csv
import pickle


def loadData(filename, readFileOverride = False):
	if not readFileOverride:
		try:
			with open('screenings.pk1', 'rb') as input:
				screenings = pickle.load(input)
		except:
			screenings = readCSV(filename)
			with open('screenings.pk1', 'wb') as output:
				pickle.dump(screenings, output)
	else:
		screenings = readCSV(filename)
	
	return screenings

def readCSV(filename):
	screenings = []
	file = open(filename)
	reader = csv.reader(file)
	firstRow = True
	for row in reader:
		if not firstRow:
			screenings.append(row)
		firstRow = False
	return screenings