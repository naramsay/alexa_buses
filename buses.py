#!/usr/bin/python
from google.transit import gtfs_realtime_pb2
import requests
import time
from datetime import datetime
import pickle
from sensitive import routes, headers, home_stop
import pytz
url = 'https://api.transport.nsw.gov.au/v1/gtfs/realtime/buses'
est = pytz.timezone('Australia/Sydney')
file_path = '/tmp/trips.pkl'



def parse_feed():
   trip_list = []  
   response = requests.get(url, headers=headers)
   feed = gtfs_realtime_pb2.FeedMessage()
   feed.ParseFromString(response.content)
   for entity in feed.entity:
      if entity.HasField('trip_update'):
         if entity.trip_update.trip.route_id in routes:
             for stops in entity.trip_update.stop_time_update:
                 if stops.stop_id == home_stop:
                    if stops.arrival.time >= time.time():
                       utc_dt = datetime.utcfromtimestamp(stops.arrival.time).replace(tzinfo=pytz.utc)
                       dt = utc_dt.astimezone(est)                       
                       arrival = dt.strftime('%H:%M')
                       route = entity.trip_update.trip.route_id[5:]
                       trip = str(arrival) + " " + str(route) + ","
                       trip_list.append(trip)
                       trip_list.sort()
   return trip_list


def save_data():
   trip_list = parse_feed()
   now = time.time()
   with open(file_path, 'w') as f:
      pickle.dump(now, f)
      pickle.dump(trip_list, f)
