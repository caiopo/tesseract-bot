import telegram
import time
import util
import pytesseract
try:
	import Image
except ImportError:
	from PIL import Image



help_text = """
Send me an image and I will run Google's Tesseract OCR tool on it and send you back the results.

You can change the language I use on Tesseract by sending me `/lang <lang_code>`.

The <lang_code> must be one of the following codes:

Code|Language
----|--------
eng | English
por | Portuguese
spa | Spanish
fra | French
ita | Italian
jpn | Japanese
"""

lang_dict = {}

default_lang = 'por'

available_langs = {'eng' : 'English',
					'por' : 'Portuguese',
					'spa' : 'Spanish',
					'fra' : 'French',
					'ita' : 'Italian',
					'jpn' : 'Japanese',
					}


def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Hello! I'm Tesseract Bot!\n\n"+help_text)

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=help_text)

def unknown(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def message(bot, update):
	photoFile = bot.getFile(update.message.photo[-1].file_id)

	filename = 'photos/photo_'+''.join(str(time.time()).split('.'))+'.jpg'

	photoFile.download(filename)

	language = lang_dict.get(update.message.chat_id, default_lang)

	image_text = pytesseract.image_to_string(Image.open(filename), 	language)

	# image_text = util.run_tesseract(filename, language)

	print(image_text)

	bot.sendMessage(chat_id=update.message.chat_id, text=image_text)

def lang(bot, update):
	try:
		_, language = update.message.text.split(' ')
	except Exception:
		try:
			current_language = available_langs[lang_dict[update.message.chat_id]]
			bot.sendMessage(chat_id=update.message.chat_id, text='Your current language is {}.'.format(current_language))
		except KeyError:
			bot.sendMessage(chat_id=update.message.chat_id, text='Your current language is Default ({}).'.format(available_langs[default_lang]))

	else:
		if language in available_langs:
			lang_dict[update.message.chat_id] = language
			bot.sendMessage(chat_id=update.message.chat_id, text='Your language is now {}.'.format(available_langs[language]))
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text="This language isn't available.")

def _something_wrong(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text='Something went wrong')
	traceback.print_exc()