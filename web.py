import os
import requests
from flask import Flask
from flask import request
from threading import Thread

# app = Flask(__name__)
app = Flask('')

@app.route('/')
def home():
	return 'We are not able to provide any information about your word. Please confirm that the word is spelled correctly or try the search again at a later time.'

def run():
  app.run(
      host = '0.0.0.0',
      port = 80
      )

def keep_alive():
  t = Thread(target=run)
  t.start()
