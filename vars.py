"""
	These tags represent values that can be used to uniquely fingerprint an image.
	Their values should be normalized so we can compute them quantitatively.
"""
target_tags = [
	('0x0201', 'ThumbnailOffset'),
	('0x0202', 'ThumbnailLength'),
	('0x0131', 'Software'),
	('0x0000', 'GPSVersion'),
	('0x010f', 'Make'),
	('0x0110', 'Model'),
	('0xa420', 'ImageUniqueID'),	# (is pervasive; survived photoshopping)
	('0xa005', 'Interoperability'),	# (changed with photoshopping)
	('0x8769', 'ExifIFDPointer'),	# (in a different place after photoshopping)
	('0x8825', 'GpsInfoIFDPointer')	# (in a different place after photoshopping)
]

