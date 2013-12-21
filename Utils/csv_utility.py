import csv, os, re
from Levenshtein import distance

from vars import ideal_tiff, TiffAspect, delimiter, quotechar, quoting, missing_value
from conf import output_dir

def analyzeTiff(file):
	tiff_re = '%s(\s+)%s(\s+)\dx\d(\s+).+(\s+)\((.*)\)'
	tiff_aspects = []
	
	for tiff in [(t.tag_position, t.label, t.type, t.ideal) for t in ideal_tiff]:
		value = missing_value
		with open(file, 'rb') as f:
			for line in f:
				match = re.findall(re.compile(tiff_re % (tiff[0], tiff[1])), line.strip())
				if len(match) == 1:
					values = [m.strip() for m in list(match[0]) if re.match(r'(\s)+', m) is None]
					if len(values) == 1:
						value = values[0].replace("\"", '')
						if tiff[2] == str:
							# take levenshtein distance from ideal value
							value = "%.9f" % (distance(tiff[3], value))
						
						break
		
		tiff_aspects.append(TiffAspect(tiff[0], tiff[1], value, tiff[2]))
	
	if len(tiff_aspects) > 0:
		return tiff_aspects
	
	return None

def index(base, output="training_data.csv"):
	with open(os.path.join(output_dir, output), 'a') as csv_file:
		tiff_csv = csv.writer(csv_file, delimiter=delimiter,
			quotechar=quotechar, quoting=quoting)
		
		corresponding_file = None
		values = None
	
		for root, dir, files in os.walk(base):
			for file in files:
				if re.match(r'[^high_|low_|med_|thumb_].*\.(jpg|mkv)', file):
					corresponding_file = os.path.join(root, file)
		
				if re.match(r'.*\.tiff\.txt', file):
					tiff = analyzeTiff(os.path.join(root, file))
					if tiff is not None:
						values = [t.ideal for t in tiff]
	
			if corresponding_file is not None and values is not None:
				values.append(os.path.join(root, corresponding_file))
				tiff_csv.writerow(values)

def indexAll(homedir, output="training_data.csv"):
	with open(os.path.join(output_dir, output), 'wb+') as csv_file:
		tiff_csv = csv.writer(csv_file, delimiter=delimiter, 
			quotechar=quotechar, quoting=quoting)
	
		labels = [tiff.label for tiff in ideal_tiff]
		labels.append("AssetPath")
		tiff_csv.writerow(labels)
	
	index(homedir)