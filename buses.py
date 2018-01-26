#!/usr/bin/python
from google.transit import gtfs_realtime_pb2
import requests
import time
import pickle
from sensitive import routes, headers, home_stop
url='https://api.transport.nsw.gov.au/v1/gtfs/realtime/buses'



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
                       arrival = time.strftime('%H:%M', time.localtime(stops.arrival.time))
                       route = entity.trip_update.trip.route_id[5:]
                       trip = str(arrival) + " " + str(route) + ","
                       trip_list.append(trip)
                       trip_list.sort()
   return trip_list


def save_data():
   trip_list = parse_feed()
   now = time.time()
   with open('trips.pkl', 'w') as f:
      pickle.dump(now, f)
      pickle.dump(trip_list, f)

save_data()
