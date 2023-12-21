from telegram import Bot
from flask import Flask
from os import getenv

bot = Bot(token=getenv("6976943825:AAEGbaD35rQICpwv8IQGKadpwy5QpStQgqI"))

app = Flask(__name__)


