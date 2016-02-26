import telegram
import time
import pytesseract
import config
import os

try:
	import Image
except ImportError:
	from PIL import Image

help_text = """
Send me an image and I will run Google's Tesseract OCR tool on it and send you back the results.

You can change the language I use on Tesseract by sending me `/lang <code>`.

The <code> must be one of the following codes:

Code -> Language
eng  -> English
por  -> Portuguese
spa  -> Spanish
fra  -> French
ita  -> Italian
jpn  -> Japanese
"""

# /setcommands
# lang - query or set your current language

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
	bot.sendMessage(chat_id=update.message.chat_id, text="Hello! I'm Tesseract Bot!\n\n"+help_text, parse_mode=telegram.ParseMode.MARKDOWN)

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=help_text, parse_mode=telegram.ParseMode.MARKDOWN)

def unknown(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def message(bot, update):

	try:
		photoFile = bot.getFile(update.message.photo[-1].file_id)

		filename = config.CACHE_DIR+'/photo_'+''.join(str(time.time()).split('.'))+'.jpg'

		photoFile.download(filename)

		language = lang_dict.get(update.message.chat_id, default_lang)

		image_text = pytesseract.image_to_string(Image.open(filename), language)

		if config.CACHE_TEMP:
			os.remove(filename)

		bot.sendMessage(chat_id=update.message.chat_id,
						text='Parsed in {}:\n\n```\n{}\n```'.format(available_langs[language], _sanitize_string(image_text)),
						parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		_something_wrong(bot, update, e)


def lang(bot, update):
	try:
		_, language = update.message.text.split(' ')
	except ValueError:

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

def _something_wrong(bot, update, e):
	bot.sendMessage(chat_id=update.message.chat_id, text='Something went wrong...\nError type: {}\nError message: {}'.format(type(e), e))
	# traceback.print_exc()
	print('deu erro:')
	print(e, e.errno, e.strerror)

def _sanitize_string(string):
	illegal_chars = '_*`[]()\\'

	sanitized = ''

	for char in string:
		sanitized += '\\' + char if char in illegal_chars else char

	return sanitized
