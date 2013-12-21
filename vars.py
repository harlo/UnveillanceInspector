"""
	These tags represent values that can be used to uniquely fingerprint an image.
	Their values should be normalized so we can compute them quantitatively.
	
	Some of these values might not exist.
	(tag_position, label, ideal_value)
	
	NOTES:
		- ImageUniqueID: is pervasive; survived photoshopping
		- Interoperability: changed with photoshopping
		- ExifIFDPointer: in a different place after photoshopping
		- GpsInfoIFDPointer: in a different place after photoshopping
	
"""
from collections import namedtuple
from conf import tiff_ideals as ideal
import csv

TiffAspect = namedtuple('TiffAspect', 'tag_position label ideal type')
ideal_tiff = [
	TiffAspect('0x0201', 'ThumbnailOffset', ideal['THUMBNAIL_OFFSET'], int),
	TiffAspect('0x0131', 'Software', ideal['SOFTWARE'], str),
	TiffAspect('0x0000', 'GPSVersion', ideal['GPS_VERSION'], str),
	TiffAspect('0x010f', 'Make', ideal['MAKE'], str),
	TiffAspect('0x0110', 'Model', ideal['MODEL'], str),
	TiffAspect('0xa420', 'ImageUniqueID', ideal['IMAGE_UNIQUE_ID'], str),
	TiffAspect('0xa005', 'Interoperability', ideal['INTEROPERABILITY'], str),
	TiffAspect('0x8769', 'ExifIFDPointer', ideal['EXIF_IFD_POINTER'], str),
	TiffAspect('0x8825', 'GpsInfoIFDPointer', ideal['GPS_INFO_IFD_POINTER'], str)
]

delimiter = ' '
quotechar = '|'
quoting = csv.QUOTE_MINIMAL