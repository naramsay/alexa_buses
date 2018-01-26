#!/usr/bin/python
from google.transit import gtfs_realtime_pb2
import requests
import time
import pickle
url='https://api.transport.nsw.gov.au/v1/gtfs/realtime/buses'
headers= {'Authorization' : 'apikey MN1Z52Ww3dwBxyKOvOOBQbJio5wup7GKCEts', 'Accept' : 'application/x-google-protobuf'}
routes=("2440_178", "2440_180", "2440_E75", "2440_E76", "2440_E77", "2440_E78", "2440_E79")
home_stop="210028"



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
