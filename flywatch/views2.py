# from django.http import HttpResponse
# from django.shortcuts import render
# import subprocess
# from playwright.sync_api import sync_playwright
# import math
# import os
# from twilio.rest import Client
# from twilio.twiml.voice_response import VoiceResponse
# import time

# account_sid = ''
# auth_token = ''
# client = Client(account_sid, auth_token)


# # C17 Registrations

# C17Regs = ['VUAUA','VUAUB','VUAUC','VUAUD','VUAUE','VUAUF','VUAUG','VUAUH','VUAUI','VUAUJ','VUAUK']

# # Radius of the Earth in miles
# R = 3959

# def haversine(lat1, lon1, lat2, lon2):
#     """
#     Calculate the great-circle distance in miles between two points
#     on the Earth's surface given by their latitude and longitude.
#     """
#     # Convert latitude and longitude from degrees to radians
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

#     # Haversine formula
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     distance = R * c
#     return distance

# def is_within_radius(lat1, lon1, lat2, lon2, radius=100):
#     """
#     Check if the given latitude and longitude (lat2, lon2) are within
#     the specified radius (default 100 miles) of the reference point (lat1, lon1).
#     """
#     distance = haversine(lat1, lon1, lat2, lon2)
#     if distance <= radius:
#         return True  # The location is within the radius
#     else:
#         return False  # The location is outside the radius

# def index(request):

#     city_lat = 22.310696
#     city_lon = 73.192635  
#     target_lat = ""
#     target_lon = "" 
#     # aircraftReg = 'VUMAF'
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, timeout=60000)  # Timeout set to 60 seconds
#         page = browser.new_page()

#         for regs in C17Regs:

#             page.goto(f"https://www.radarbox.com/data/flights/{regs}")
#             page.wait_for_load_state('load')
#             print(page.title())  # This will print the title of the page
#             # latitude = page.locator('.sc-pbvqsk-0 btLBKZ').text_content().strip()

#             time.sleep(3)
#             target_lat_str = page.locator('div#title:has-text("Latitude")').locator('xpath=following-sibling::div[@id="value"]').text_content().strip()
#             target_lon_str = page.locator('div#title:has-text("Longitude")').locator('xpath=following-sibling::div[@id="value"]').text_content().strip()

#             print("C17's Latitude ", target_lat_str)
#             print("C17's Longitude", target_lon_str)
#             if '-' in target_lat_str and '-' in target_lon_str:

#                 target_lat = float(target_lat_str.replace("-", ""))
#                 target_lon = float(target_lon_str.replace("-", ""))
            
#             elif '-' in target_lat_str:
#                 target_lat = float(target_lat_str.replace("-", ""))
#                 target_lon = float(target_lon_str)
#             elif '-' in target_lon_str:
#                 target_lon = float(target_lon_str.replace("-", ""))
#                 target_lat = float(target_lat_str)
                
#             else:
#                 target_lat = float(target_lat_str)
#                 target_lon = float(target_lon_str)

#             print(f"Latitude of the aircraft: {target_lat}")
#             print(f"Latitude of the aircraft: {target_lon}")

#             if is_within_radius(city_lat, city_lon, target_lat, target_lon):
#                 print(f"{regs} is within 100 miles of Vadodara (Lat : {city_lat} , long {city_lon}).")

#                 response = VoiceResponse()
#                 response.say(f"Hello, this is a call from Mr. Donkey's system. Indian Air Force's C17 with Registration {regs} is within 100 miles of Vadodara Last Tracked Position of {regs} is {target_lat} {target_lon} . ", voice="alice")
#                 call = client.calls.create(
#                 url="http://demo.twilio.com/docs/voice.xml",
#                 to="+919909471247",
#                 from_="+15017122661",
#                 twiml=str(response)
# )
#             else:
#                 print(f"{regs} is NOT within 100 miles of Vadodara (Lat : {city_lat} , long {city_lon}).")

#                 response = VoiceResponse()
#                 response.say(f"Hello, this is a call from Mr. Donkey's system. Indian Air Force's C17 with Registration {regs} is within 100 miles of Vadodara Last Tracked Position of {regs} is {target_lat} {target_lon} . ", voice="alice")

#                 # call = client.calls.create(
#                 # url="http://demo.twilio.com/docs/voice.xml",
#                 # to="+919909471247",
#                 # from_="+17756187371",
#                 # twiml=str(response)
#                 # )

#     browser.close()

#     return render(request, "index.html")

from django.http import HttpResponse
from django.shortcuts import render
import subprocess
from playwright.sync_api import sync_playwright
import math
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import time

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

# C17 Registrations
C17Regs = ['VUAUA', 'VUAUB', 'VUAUC', 'VUAUD', 'VUAUE', 'VUAUF', 'VUAUG', 'VUAUH', 'VUAUI', 'VUAUJ', 'VUAUK']

# Radius of the Earth in miles
R = 3959


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def is_within_radius(lat1, lon1, lat2, lon2, radius=100):
    distance = haversine(lat1, lon1, lat2, lon2)
    return distance <= radius


def perform_check():
    city_lat = 22.310696
    city_lon = 73.192635
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, timeout=60000)
        page = browser.new_page()

        for regs in C17Regs:
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
                    print(f"{regs} is within 100 miles of Vadodara.")
                    response = VoiceResponse()
                    response.say(
                        f"Hello, this is a call from Mr. Donkey's system. Indian Air Force's C17 with Registration {regs} "
                        f"is within 100 miles of Vadodara at Lat {target_lat} and Lon {target_lon}.",
                        voice="alice"
                    )
                    client.calls.create(
                        url="http://demo.twilio.com/docs/voice.xml",
                        to="+919909471247",
                        from_="+15017122661",
                        twiml=str(response)
                    )
                else:
                    print(f"{regs} is NOT within 100 miles of Vadodara.")

            except Exception as e:
                print(f"Error with processing aircraft {regs}: {e}")

        browser.close()


while True:
    try:
        perform_check()
        print("Execution completed. Sleeping for 15 minutes...")
        time.sleep(15 * 60)  # Sleep for 15 minutes
    except Exception as e:
        print(f"Error in execution: {e}")
        time.sleep(15 * 60)  # Sleep even on error


