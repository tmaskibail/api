import googlemaps

# Again, we need to specify an API key for authorization
gmapsAPIKey = 'AIzaSyCUMMUIy73ysfvKcUTVOsv1ITWD9ojagN4'
gmaps = googlemaps.Client(key=gmapsAPIKey)

# We will also load some modules to handle dates and times
from datetime import datetime
from datetime import timedelta


# As the response of gmaps is different for the different modes of transportation
# we need to create multiple functions to harmonize this

# First a function to get the required information for driving
def getDrivingDuration(start, destination):
    directions_result = gmaps.directions(
                        start,
                        destination,
                        mode="driving",
                        departure_time='now')
    duration = directions_result[0]["legs"][0]["duration_in_traffic"]["text"]
    duration_value = directions_result[0]["legs"][0]["duration_in_traffic"]["value"]
    arrival_time = datetime.now()+timedelta(seconds=duration_value)+timedelta(hours=2)
    print("By car the trip will take " + duration
          + ". If you start now you will arrive at "+ str(arrival_time))
    return duration, arrival_time

# Second a function to get the required information for walking
def getWalkingDuration(start, destination):
    directions_result = gmaps.directions(
                        start,
                        destination,
                        mode="walking",
                        departure_time='now')
    duration = directions_result[0]["legs"][0]["duration"]["text"]
    duration_value = directions_result[0]["legs"][0]["duration"]["value"]
    arrival_time = datetime.now()+timedelta(seconds=duration_value)+timedelta(hours=2)
    print("Walking will take " + duration
      + ". If you start now you will arrive at "+ str(arrival_time))
    return duration, arrival_time

# And third a function to get the required information for walking
def getTransitDuration(start, destination):
    directions_result = gmaps.directions(
                    start,
                    destination,
                    mode="transit",
                    departure_time='now')
    duration = directions_result[0]["legs"][0]["duration"]["text"]
    duration_value = directions_result[0]["legs"][0]["duration"]["value"]
    arrival_time = datetime.fromtimestamp(directions_result[0]["legs"][0]["arrival_time"]["value"])+timedelta(hours=2)
    print("With public transport the trip will take " + duration
      + ". If you start now you will arrive at "+ str(arrival_time))
    return duration, arrival_time
