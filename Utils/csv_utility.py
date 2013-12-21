import csv, os, re

from vars import ideal_tiff, TiffAspect
from conf import output_dir

def analyzeTiff(file):
	tiff_re = '%s(\s+)%s(\s+)\dx\d(\s+).+(\s+)\((.*)\)'
	tiff_aspects = []
	
	for tiff in [(t.tag_position, t.label, t.type) for t in ideal_tiff]:
		value = "n/a"
		with open(file, 'rb') as f:
			for line in f:
				match = re.findall(re.compile(tiff_re % (tiff[0], tiff[1])), line.strip())
				if len(match) == 1:
					values = [m.strip() for m in list(match[0]) if re.match(r'(\s)+', m) is None]
					if len(values) == 1:
						value = values[0].replace("\"", '')
						break
		
		tiff_aspects.append(TiffAspect(tiff[0], tiff[1], value, tiff[2]))
	
	if len(tiff_aspects) > 0:
		return tiff_aspects
	
	return None

def indexAll(homedir):
	with open(os.path.join(output_dir, 'test.csv'), 'wb+') as csv_file:
		tiff_csv = csv.writer(csv_file, delimiter=' ', 
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
	
		labels = [tiff.label for tiff in ideal_tiff]
		labels.append("AssetPath")
		tiff_csv.writerow(labels)

		for root, dir, files in os.walk(homedir):
			corresponding_file = None
			values = None

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