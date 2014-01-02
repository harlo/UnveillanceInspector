import csv, os, re, string
from Levenshtein import ratio

from vars import ideal_tiff, TiffAspect, delimiter, quotechar, quoting, missing_value, labels
from conf import output_dir

def analyzeTiff(file):
	numbers = str("".join([str(i) for i in range(0,10)]))
	tiff_re = '%s\s+%s\s+\d+x\d+\s+.+\s+\((.*)\)'
	tiff_aspects = []
	
	for tiff in [(t.tag_position, t.label, t.ideal, t.type) for t in ideal_tiff]:
		value = missing_value
		ideal = tiff[2]
		pattern = tiff_re % (tiff[0], tiff[1])
		
		if tiff[2] is None:
			if tiff[3] == str:
				ideal = string.letters + numbers
			elif tiff[3] == int:
				ideal = int(numbers)
				
		with open(file, 'rb') as f:
			for line in f:
				match = re.findall(re.compile(pattern), line.strip())
				if len(match) == 1:
					if tiff[3] == str:
						# take levenshtein ratio from ideal value
						value = "%.9f" % ratio(ideal, str(match[0].replace("\"", '')))
					elif tiff[3] == int:
						# or take the ratio from ideal value
						value = ideal/float(match[0].replace("\"", ''))
					break

		if value == missing_value:
			if tiff[2] is None:
				value = 1
			else:
				value = 0

		tiff_aspects.append(TiffAspect(tiff[0], tiff[1], value, tiff[2]))
	
	if len(tiff_aspects) > 0:
		return tiff_aspects
	
	return None

def analyzeGPGMessage(file):
	return True

def index(base, output="training_data.csv"):
	with open(os.path.join(output_dir, output), 'a') as csv_file:
		tiff_csv = csv.writer(
			csv_file, delimiter=delimiter,
			quotechar=quotechar, quoting=quoting)
		
		corresponding_file = None
		values = None
		has_j3m = False
		was_encrypted = False
	
		for root, dir, files in os.walk(base):
			for file in files:
				if re.match(r'[^high_|low_|med_|thumb_].*\.(jpg|mkv)', file):
					corresponding_file = os.path.join(root, file)
		
				if re.match(r'.*\.tiff\.txt', file):
					tiff = analyzeTiff(os.path.join(root, file))
					if tiff is not None:
						values = [t.ideal for t in tiff]
				
				if re.match(r'.*\.j3m$', file):
					has_j3m = True
				
				if re.match(r'.*\.txt.unb64$', file):
					was_encrypted = analyzeGPGMessage(os.path.join(root, file))
	
			if corresponding_file is not None and values is not None:
				values.append(1.0 if has_j3m else 0.0)
				values.append(1.0 if was_encrypted else 0.0)
				values.append(os.path.join(root, corresponding_file))
				tiff_csv.writerow(values)

def indexAll(homedir, output="training_data.csv"):
	with open(os.path.join(output_dir, output), 'wb+') as csv_file:
		tiff_csv = csv.writer(csv_file, delimiter=delimiter, 
			quotechar=quotechar, quoting=quoting)
	
		tiff_csv.writerow(labels)
	
	index(homedir, output=output)

def createTrainingDataset(homedir):
	# iterate over submissions: some will be training data, some will be test data
	
	# index all training data
	
	# index all test data
	
	pass