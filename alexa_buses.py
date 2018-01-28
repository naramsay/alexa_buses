#!/usr/bin/python

import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import time
import pickle
import buses
import os.path


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
file_path='/tmp/trips.pkl'
cache_expiry = 90 # in seconds


def freshness():
   now = int(time.time())
   if not os.path.exists(file_path):
      get_data()
   result_tuple = parse_cache()
   cache_age = result_tuple[0]
   if int(cache_age) < now - cache_expiry:
      get_data()
      result_tuple = parse_cache()
   return result_tuple[1]


def get_data():
   print "Updating cache"
   buses.save_data()


def parse_cache():
   print "Parsing cache"
   with open(file_path, 'r') as f:
      cache_age = pickle.load(f)
      next_buses_list =  pickle.load(f)
   return (cache_age, next_buses_list)
      

@ask.intent("NextBuses")
def next_buses():
    next_buses_list = freshness()
    result = next_buses_list[0:3]
    result = ' '.join(result)
    return statement(result)


@ask.intent("NextnBuses", convert={'Number' : int})
def next_n_buses(Number):
    next_buses_list = freshness()
    result = next_buses_list[0:Number]
    result = ' '.join(result)
    return statement(result)


if __name__ == '__main__':

    app.run(debug=True)
