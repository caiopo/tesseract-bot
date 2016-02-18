import os
import pytesseract
try:
	import Image
except ImportError:
	from PIL import Image


def delete_file(filename):
	os.remove('photos/'+filename)

def run_tesseract(filename, lang):
	return pytesseract.image_to_string(Image.open(filename), lang=lang)

if __name__ == '__main__':
	print(run_tesseract('photos/photo_1455708694.319482.jpg', 'por'))