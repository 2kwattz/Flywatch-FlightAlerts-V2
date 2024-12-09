from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import subprocess
from playwright.sync_api import sync_playwright
import math
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import time
from celery import shared_task
from celery.result import AsyncResult
import threading
from channels.layers import get_channel_layer
import json
from threading import Lock
import asyncio
import websockets


account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
task_status = {"status": "Not Started", "result": None}

shared_dict = {
    'VUAUA': False,
    'VUAUB': False,
    'VUAUC': False,
    'VUAUD': False,
    'VUAUE': False,
    'VUAUF': False,
    'VUAUG': False,
    'VUAUH': False,
    'VUAUI': False,
    'VUAUJ': False,
    'VUAUK': False
}

lock = Lock()


# C17 Registrations

Regs = ['VUAUA','VUAUB','VUAUC','VUAUD','VUAUE','VUAUF','VUAUG','VUAUH','VUAUI','VUAUJ','VUAUK']

# Radius of the Earth in miles
R = 3959

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance in miles between two points
    on the Earth's surface given by their latitude and longitude.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def is_within_radius(lat1, lon1, lat2, lon2, radius=100):
    """
    Check if the given latitude and longitude (lat2, lon2) are within
    the specified radius (default 100 miles) of the reference point (lat1, lon1).
    """
    distance = haversine(lat1, lon1, lat2, lon2)
    if distance <= radius:
        return True  # The location is within the radius
    else:
        return False  # The location is outside the radius

def perform_check():
    city_lat = 22.310696
    city_lon = 73.192635

    # Delhi
    # city_lat = 28.644800
    # city_lon = 77.216721
      
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, timeout=60000)
        page = browser.new_page()

        for regs in Regs:
            page.goto(f"https://www.radarbox.com/data/flights/{regs}")
            page.wait_for_load_state('load')
            time.sleep(2)
            
            try:
                target_lat_str = page.locator('div#title:has-text("Latitude")').locator(
                    'xpath=following-sibling::div[@id="value"]').text_content().strip()
                target_lon_str = page.locator('div#title:has-text("Longitude")').locator(
                    'xpath=following-sibling::div[@id="value"]').text_content().strip()

                # Parse latitude/longitude
                target_lat = float(target_lat_str)
                target_lon = float(target_lon_str)

                if is_within_radius(city_lat, city_lon, target_lat, target_lon):
                    print(f"C17 Registration {regs} is within 100 miles of Vadodara. LAT {target_lat} {target_lon} \n")
                    print(f"Initiating VoIP Call Alert for +91 9909471247\n")
                    print(f"Triggering Buzzer Alert on ESP8266 Microprocessor\n")
                    response = VoiceResponse()
                    response.say(
                        f"Hello, this is a call from Mr. Donkey's system. Indian Air Force's C17 with Registration {regs} "
                        f"is within 100 miles of Vadodara at Lat {target_lat} and Lon {target_lon}.",
                        voice="alice"
                    )
                    client.calls.create(
                        url="http://demo.twilio.com/docs/voice.xml",
                        to="+919909471247",
                        from_="+17756187371",
                        twiml=str(response)
                    )
                    
                    with lock:
                        print("Updating dictionary...")
                        shared_dict[regs] = True

                        print("Values in shared dict", shared_dict)
                else:
                    print(f"\n{regs} is NOT within 100 miles of Vadodara.")
                    print(f"C17 {regs} LAT LONG {target_lat} {target_lon} . Vadodara's LAT LONG {city_lat} {city_lon}")

                    with lock:
                        print("Updating dictionary...")
                        shared_dict[regs] = False

                        print("Values in shared dict", shared_dict)

            except Exception as e:
                print(f"Error with processing aircraft {regs}: {e}")

        browser.close()


def run_periodic_task():
    global task_status
    while True:
        try:
            task_status["status"] = "Task Started"
            task_status["result"] = "Running"
            perform_check()
            task_status["status"] = "Task Finished"
            task_status["result"] = "Code Executed. Sleeping for 15min"

            print("Code executed. Sleeping for 15min")
        except Exception as e:
            task_status["status"] = "Error"
            task_status["result"] = str(e)

        # Sleep for 15 minutes (900 seconds) before running again
        time.sleep(900)

def start_task():
    task_thread = threading.Thread(target=run_periodic_task)
    task_thread.daemon = True  # Run as a daemon thread so it won't block the server
    task_thread.start()

if task_status["status"] == "Not Started":
        start_task()  # Start the task if not already running



def index(request):

    city_lat = 22.310696
    city_lon = 73.192635  
    target_lat = ""
    target_lon = "" 


    

    # return render(request, "index.html")
    return render(request, "index.html", {'task_status': task_status})





