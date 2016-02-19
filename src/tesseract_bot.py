#! /usr/bin/env python3

import logging
import handler
import argparse
import config
import errno
import os
from telegram import Updater

def resolve_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
	resolve_args()

	try:
	    os.mkdir(config.CACHE_DIR)
	except OSError:
	    if e.errno != errno.EEXIST:
	        raise

	updater = Updater(token=config.BOT_TOKEN)

	dispatcher = updater.dispatcher

	print(updater.bot.getMe())

	dispatcher.addTelegramCommandHandler('start', handler.start)
	dispatcher.addTelegramCommandHandler('help', handler.help)
	dispatcher.addTelegramCommandHandler('lang', handler.lang)

	dispatcher.addTelegramMessageHandler(handler.message)

	dispatcher.addUnknownTelegramCommandHandler(handler.unknown)

	updater.start_polling()

if __name__ == '__main__':
	main()