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
Send me an image and I will run Google's Tesseract OCR tool on it \
and send you back the results.

You can change the language I use on Tesseract by sending me `/lang <code>`.

The <code> must be one of the following codes:

Code -> Language
eng  -> English
por  -> Portuguese
spa  -> Spanish
fra  -> French
ita  -> Italian
jpn  -> Japanese

In groups, I will not automatically parse the images, \
I will wait for someoneto use the /tesseract command, \
then I'll parse the last image sent.

Made by caiopoliveira@gmail.com
Source on https://github.com/caiopo/tesseract-bot
"""

# /setcommands
# lang - query or set your current language
# help - detailed information about the bot

DEFAULT_LANG = 'por'

lang_dict = {}

group_photos = {}

available_langs = {'eng' : 'English',
					'por' : 'Portuguese',
					'spa' : 'Spanish',
					'fra' : 'French',
					'ita' : 'Italian',
					'jpn' : 'Japanese',
					}

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id,
		text="Hello! I'm Tesseract Bot!\n\n"+help_text,
		parse_mode=telegram.ParseMode.MARKDOWN,
		disable_web_page_preview=True)

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id,
		text=help_text,
		parse_mode=telegram.ParseMode.MARKDOWN,
		disable_web_page_preview=True)

def unknown(bot, update):
	if update.message.chat_id > 0: # user	
		bot.sendMessage(chat_id=update.message.chat_id,
			text="Sorry, I didn't understand that command.")

def message(bot, update):
	if not update.message.photo:
		return

	photosize = bot.getFile(update.message.photo[-1].file_id)

	if update.message.chat_id > 0: # user	
		_photosize_to_parsed(bot, update, photosize)

	else: # group
		group_photos[update.message.chat_id] = photosize


def lang(bot, update):
	try:
		_, language = update.message.text.split(' ')
	except ValueError:

		try:
			current_language = available_langs[lang_dict[update.message.chat_id]]
			bot.sendMessage(chat_id=update.message.chat_id, text='Your current language is {}.'.format(current_language))
		except KeyError:
			bot.sendMessage(chat_id=update.message.chat_id, text='Your current language is Default ({}).'.format(available_langs[DEFAULT_LANG]))

	else:
		if language in available_langs:
			lang_dict[update.message.chat_id] = language
			bot.sendMessage(chat_id=update.message.chat_id, text='Your language is now {}.'.format(available_langs[language]))
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text="This language isn't available.")


def tesseract(bot, update):
	if update.message.chat_id > 0:
		bot.sendMessage(chat_id=update.message.chat_id, text='/tesseract command is only available to groups.')
	else:
		_photosize_to_parsed(bot, update, group_photos[update.message.chat_id])


def _photosize_to_parsed(bot, update, photosize):
	try:
		filename = config.CACHE_DIR+'/photo_'+''.join(str(time.time()).split('.'))+'.jpg'

		photosize.download(filename)

		language = lang_dict.get(update.message.chat_id, DEFAULT_LANG)

		image_text = pytesseract.image_to_string(Image.open(filename), language)

		if config.CACHE_TEMP:
			os.remove(filename)

		sanitized_string = _sanitize_string(image_text)

		if sanitized_string:
			response_msg = 'Parsed in {}:\n\n```\n{}\n```'.format(
				available_langs[language], sanitized_string)
		else:
			response_msg = 'Nothing found! :(\nParsed in {}'.format(available_langs[language])

		bot.sendMessage(chat_id=update.message.chat_id,
						text=response_msg,
					parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		_something_wrong(bot, update, e)

def _something_wrong(bot, update, e):
	bot.sendMessage(chat_id=update.message.chat_id, text='Something went wrong...\nError type: {}\nError message: {}'.format(type(e), e))

def _sanitize_string(string):
	illegal_chars = '_*`[]()\\'

	sanitized = ''

	for char in string:
		sanitized += '\\' + char if char in illegal_chars else char

	return sanitized
