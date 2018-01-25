#!/usr/bin/env python

# from telegram import ChatAction
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import RPi.GPIO as GPIO
import time

import config

secret = config.secret
ALLOWED_USERS = config.ALLOWED_USERS
proxyurl = config.proxyurl

updater = Updater(token=secret, request_kwargs={'proxy_url': config.proxyurl})
dispatcher = updater.dispatcher

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

def makecoffee():
    GPIO.output(26, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(26, GPIO.LOW)


def start(bot, update):
    msg = "Foobar!!!"
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def whoami(bot, update):
    msg = "You're {}".format(update.effective_user.id)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def coffee(bot, update, args):
    user_id = update.effective_user.id
    if user_id in ALLOWED_USERS:
        # msg = "You're allowed to get some coffee ;)"
        if args:
            try:
                sec = int(''.join(args)) % 60
                bot.sendMessage(chat_id=update.message.chat_id, text="Warten Sie {}, Ende!".format(sec))
                time.sleep(sec)
                bot.sendMessage(chat_id=update.message.chat_id, text="Coffee is in the making ;)")
            except ValueError:
                pass
        makecoffee()
    else:
        msg = "Get outta here..."
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('coffee', coffee, pass_args=True))
dispatcher.add_handler(CommandHandler('whoami', whoami))

updater.start_polling()
updater.idle()
