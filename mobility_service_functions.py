import google_api_functions as gfunc
from datetime import datetime
import requests
import json


url = "http://api.openweathermap.org/data/2.5/weather"

def getWeather(location):
  parameter = {
    'APPID': '21d450d89671b5620fe0a6d091d263f5',
    'units': 'metric',
    'q': location
  }
  response = requests.get(url, params=parameter)
  temperature = response.json()['main']['temp']
  weather = response.json()['weather'][0]['description']
  print("The temperature in "+location.capitalize()+" is "+str(temperature) + " degrees with "+weather)
  return temperature, weather

def getBestTransport(start, destination, desired_arrival_time, acceptable_walking_weather, minimum_walking_temperature, maximum_walking_temperature):
    # Define the weather conditions you would walk in
    
    # Parse the arrival time
    desired_arrival_time = datetime.strptime(desired_arrival_time, "%Y.%m.%d %H:%M")

    # Get the current weather for starting location
    cityArray = start.split(', ')
    temperature, weather_condition = getWeather(cityArray[1].strip())
    
    # Check if weather is acceptable for walking
    walking_weather = (temperature >= minimum_walking_temperature and
       temperature <= maximum_walking_temperature and
       weather_condition in acceptable_walking_weather)
    
    # Write the weather report
    if(walking_weather):
        weather_report = "The weather is fine with " + str(temperature) + " degrees and " + weather_condition
    else:
        weather_report = "Unfortunately the weather is bad with " + str(temperature) + " degrees and " + weather_condition 
    

    # Check if the weather is fine and if we would arrive in time
    duration, arrival_time = gfunc.getWalkingDuration(start,destination)
    if (walking_weather and arrival_time <= desired_arrival_time):
        return (weather_report
            + ". The best way to get to your meeting is walking. "
            + "If you start now you will arrive at " + str(arrival_time.strftime('%H:%M'))
            + " in time for your meeting at " +str(desired_arrival_time.strftime('%H:%M')))
    
    # If the weather is not acceptable for walking, we will look for public transport
    # Check if we would arrive in time
    duration, arrival_time = gfunc.getTransitDuration(start,destination)
    if (arrival_time <= desired_arrival_time):
        return (weather_report 
            + ". The best way to get to your meeting is public transport. "
            + "If you start now you can arrive at " + str(arrival_time.strftime('%H:%M')) 
            + " in time for your meeting at " +str(desired_arrival_time.strftime('%H:%M')))
    
    # If public transport is not feasible, we will check driving by car
    # Check if we would arrive in time
    duration, arrival_time = gfunc.getDrivingDuration(start,destination)
    if (arrival_time <= desired_arrival_time):
        return (weather_report 
            + ". The best way to get to your meeting is driving by car. "
            + "If you start now you can arrive at " + str(arrival_time.strftime('%H:%M')) 
            + " in time for your meeting at " +str(desired_arrival_time.strftime('%H:%M')))
    
    # Finally we have to give up, if everything else fails
    return weather_report+ " Unfortunately no travel mode will bring you to your meeting in time."
        