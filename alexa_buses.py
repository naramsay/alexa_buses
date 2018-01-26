import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import time
import pickle
import buses


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
cache_age = int
next_buses_list = []

def freshness():
   now = int(time.time())
   parse_cache()
   p = now - 90
   c = int(cache_age)
   print "cache" + " " + str(c) + " future" + " " +  str(p)
   if int(cache_age) < now - 90:
      print "refreshing"
      buses.save_data()
      parse_cache()


def parse_cache():
   print "Parsing cache"
   with open('trips.pkl', 'r') as f:
      global cache_age
      global next_buses_list
      cache_age = pickle.load(f)
      next_buses_list =  pickle.load(f)
      

@ask.intent("NextBuses")
def next_buses():
    freshness()
    result = next_buses_list[0:3]
    result = ' '.join(result)
    return statement(result)

@ask.intent("NextnBuses", convert={'Number' : int})
def next_n_buses(Number):
    freshness()
    result = next_buses_list[0:Number]
    result = ' '.join(result)
    return statement(result)


if __name__ == '__main__':

    app.run(debug=True)
