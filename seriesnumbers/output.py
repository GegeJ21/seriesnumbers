import os
import json
import csv

def generateOutput(full_path,result):
	"""
	takes the full path to the output file and based on the chosen extension generates an output file

	:param full_path: path to the file to write
	:tyep full_path: str

	:parma result: series of number to output
	:type result: list[int]
	"""
	f = open(full_path,"w+")
	path, this_format = os.path.splitext(full_path)
	if this_format == ".txt":
		generateTxt(result, path)
	elif this_format == ".json":
		generateJson(result, path)
	elif this_format == ".cvs":
		generateCvs(result, path)

def generateJson(seq, path):
	"""
	generates json output file

	:param seq: sequence of numbers to output
	:type path: list[int]

	:param path: path to file 
	:type path: str
	"""
	data = {}
	data['numbers'] = []
	for x in range(len(seq)):
		data['numbers'].append({str(x + 1): str(seq[x])})
	with open(path + ".json", "w+") as outfile:
		json.dump(data, outfile)

def generateTxt(seq, path):
	"""
	generates txt output file

	:param seq: sequence of numbers to output
	:type path: list[int]

	:param path: path to file 
	:type path: str
	"""
	outfile = open(path + ".txt", "w+")
	for x in range(len(seq)):
		outfile.write(str(x + 1) + ": " + str(seq[x]) + "\n")
	outfile.close()

def generateCvs(seq, path):
	"""
	generates cvs output file

	:param seq: sequence of numbers to output
	:type path: list[int]

	:param path: path to file 
	:type path: str
	"""
	data = []
	for x in range(len(seq)):
		data.append(str(seq[x]))
	outfile = open(path + ".csv", "w+")
	with outfile:
		writer = csv.writer(outfile)
		writer.writerows(data)