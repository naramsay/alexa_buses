Alexa Skill that returns the next buses for your local stop.
This utilises the GTFS realtime Proto Buffer API feed provided by the NSW Government https://opendata.transport.nsw.gov.au/.
Takes a list of routes, and a home stop id and returns the next 3 or n buses.
Written to work with AWS Lambda. Use Zappa to upload to Lambda.
The cache is written to the Lamda scratch disk in /tmp/.
