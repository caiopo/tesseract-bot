# tesseract-bot
A Telegram bot to parse images with text using Google's Tesseract

Usage
-----

Copy `src/config.py.sample` to `src/config.py`.

Add your token (the one you got from [BotFather](http://telegram.me/BotFather)) to `src/config.py` then run `./src/tesseract_bot.py`.

You can also use the '-v' flag to enable verbose.

Note: you **must** have Tesseract and the Tesseract language packs installed. Tesseract is generally listed as `tesseract` or `tesseract-ocr` on most package managers.