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
from django.urls import re_path
from channels.generic.websocket import AsyncWebsocketConsumer
import random
from playwright_stealth import stealth_sync
from django.conf import settings

from threading import Timer

from datetime import datetime, timedelta

# Time interval to send requests

min_interval = 600
max_interval = 900


 # Randomize viewport size (e.g., simulate mobile or desktop screen) to mimic real user
width = random.choice([1280, 1366, 1440, 1920, 360, 412, 768])
height = random.choice([720, 800, 1080, 900, 640])




account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)
task_status = {"status": "Not Started", "result": None}

# shared_dict = {
#     'VUAUA': False,
#     'VUAUB': False,
#     'VUAUC': False,
#     'VUAUD': False,
#     'VUAUE': False,
#     'VUAUF': False,
#     'VUAUG': False,
#     'VUAUH': False,
#     'VUAUI': False,
#     'VUAUJ': False,
#     'VUAUK': False
# }

shared_dict = {
    'CB-8001': False,
    'CB-8002': False,
    'CB-8003': False,
    'CB-8004': False,
    'CB-8005': False,
    'CB-8006': False,
    'CB-8007': False,
    'CB-8008': False,
    'CB-8009': False,
    'CB-8010': False,
    'CB-8011': False
}

logs_data = {}
data_lock = Lock()
numbersToCall = ['+919909471247','+916354248126']

# C17 Registrations

Regs = ['VUAUA','VUAUB','VUAUC','VUAUD','VUAUE','VUAUF','VUAUG','VUAUH','VUAUI','VUAUJ','VUAUK']

Callsigns = ['CB-8001','CB-8002','CB-8003','CB-8004','CB-8005','CB-8006','CB-8007','CB-8008','CB8009','CB-8010']

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # Works on both Windows and Unix-based systems
    print("Console cleared.")  # Optional message after clearing

    # Schedule the next clearing after 3 hours (10800 seconds)
    Timer(10800, clear_console).start()

# Start the log clearing scheduler
# clear_console()

def trackStatus(request):
    return JsonResponse(shared_dict)

def trackLogs(request):
    return JsonResponse(logs_data)

def profile_view(request):
   return HttpResponse("Welcome to your profile page!")

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

def is_within_radius(lat1, lon1, lat2, lon2, radius=400):
    """
    Check if the given latitude and longitude (lat2, lon2) are within
    the specified radius (default 100 miles) of the reference point (lat1, lon1).
    """
    distance = haversine(lat1, lon1, lat2, lon2)
    if distance <= radius:
        return True  # The location is within the radius
    else:
        return False  # The location is outside the radius


def get_logs_in_memory(request):
    # Get the in-memory log buffer
    log_stream = settings.LOGGING['handlers']['memory']['stream']
    log_stream.seek(0)  # Go to the start of the buffer
    logs = log_stream.read()  # Read the entire buffer content
    return JsonResponse({'logs': logs.splitlines()}, safe=False)




def get_print_logs(request):
    # Access the captured print statements
    try:
        settings.PRINT_STREAM.seek(0)  # Go to the start of the stream
        logs = settings.PRINT_STREAM.read()  # Read the logs
        return JsonResponse({'print_logs': logs.splitlines()}, safe=False)
    except AttributeError:
        return JsonResponse({'error': 'Print stream not initialized'}, status=500)

def getTaskStatus(request):
    try:
        return JsonResponse(task_status)
    except Exception as e:
        return JsonResponse(e)

# def fetch_proxy():
#     with sync_playwright() as p:
#         # Launch browser (headless=True or False, depending on your needs)
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()

#         # Fetch the proxy data by sending an HTTP GET request
#         response = page.request.get('https://gimmeproxy.com/api/getProxy')
        
#         # Ensure the request was successful
#         if response.status != 200:
#             print("Failed to get proxy data.")
#             return None

#         # Parse the JSON response
#         proxy_data = response.json()

#         # Extract IP and Port from the response JSON
#         proxy_ip = proxy_data.get('ip')
#         proxy_port = proxy_data.get('port')


#         if proxy_ip and proxy_port:
#             browser.close()
#             return f"http://{proxy_ip}:{proxy_port}"
#         else:
#             print("Proxy data is incomplete.")
#             browser.close()
      
# options = { 'proxy': { 'server': 'http://brd.superproxy.io:33335',
#  'username': ' brd-customer-hl_3edebee6-zone-airnavscrap]-zone-[airnavscrap:s8np9gjapfo8]',
#   'password': '[s8np9gjapfo8]' } }

   # Access the values proxy_server = options['proxy']['server'] username = options['proxy']['username'] password = options['proxy']['password']

options = { 'proxy': { 'server': 'http://brd.superproxy.io:33335', 'username': 'brd-customer-hl_3edebee6-zone-airnavscrap', 'password': 's8np9gjapfo8' } }

proxy_server = options['proxy']['server']
username = options['proxy']['username']
password = options['proxy']['password']

def perform_check():

    # Vadodara's LAT
    city_lat = 22.310696
    city_lon = 73.192635

    # proxy_url = fetch_proxy()
    # if proxy_url:
    #     print(f"Using Proxy: {proxy_url}")

    # Delhi (for testing)
    # city_lat = 28.644800
    # city_lon = 77.216721
      
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,  
        # args=[
        #     '--no-sandbox',  # Avoid sandboxing in headless mode
        #     '--enable-accelerated-video-decode',  # Enable video decoding for h264
        #     '--disable-blink-features=AutomationControlled'
        # ],
        # proxy={"server": proxy_url},
        timeout=2100000)

        # context = browser.new_context(
        # proxy={"server": proxy_url}  # Specify proxy details if needed
        #    )
    #     browser = p.chromium.launch(headless=False,  args=[
    # '--no-sandbox',  # Avoid sandboxing in headless mode
    # '--enable-accelerated-video-decode',  # Enable video decoding for h264
    # '--disable-blink-features=AutomationControlled',
    # '--disable-gpu'  # Disable GPU hardware acceleration
    # ], timeout=60000)


        

    #     browser = p.chromium.launch(
    #     headless=False,  # Set to False if you need to see the browser, True for headless mode
    #     proxy={"server": proxy_url},  # Pass the proxy URL
    #     timeout=60000  # Timeout for launching the browser (in milliseconds)
    # )

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            ]

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cookie": "cookie_consent=true",  # Example of a cookie consent header
            }
        
        x = random.randint(50, 500)  # Random X coordinate between 50 and 500
        y = random.randint(50, 500)  # Random Y coordinate between 50 and 500

        print("Headless Browser launched")
        page = browser.new_page()
        # stealth_sync(page)


        # page.evaluate_on_new_document('''
        # Object.defineProperty(navigator, "webdriver", {get: () => false});
        # window.navigator.__defineGetter__('plugins', function(){
        # return [];
        # });
        # ''')


        page.evaluate("""
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        });
        """)

        
        # page.goto("https://bot.sannysoft.com/",timeout=170000)  # Bot detection test site
        page.wait_for_load_state('load')
        print(f"Performing Stealthcheck tests to detect bot activity before scrapping {datetime.now()}")

        # Save screenshot for validation
        # page.screenshot(path="stealth_test.png")

        # page.goto("https://www.browserscan.net/bot-detection")
        # page.screenshot(path="stealth_test2.png",timeout=170000)
        

        # for regs in Regs:
        for regs in Callsigns:
            

            user_agent = random.choice(user_agents)
            
            # Get the IP address (this will show the proxy IP being used)

            page.set_extra_http_headers({"User-Agent": user_agent})
            page.set_extra_http_headers(headers)
            # time.sleep(random.uniform(1, 3))
            page.goto(f"https://www.airnavradar.com/data/registration/{regs}",timeout=2100000)
            # page.goto(f"https://www.flightradar24.com/data/registration/{regs}",timeout=2100000)
            page.wait_for_load_state('load')
            page.set_viewport_size({"width": width, "height": height})

            page.mouse.move(x, y)  # Move mouse to random coordinates
            time.sleep(random.uniform(0.5, 1.5))  # Random human-like pause between 0.5 and 1.5 seconds
            page.mouse.click(x, y)  # Click at random coordinates
            time.sleep(random.uniform(2.5, 5.5))
            # time.sleep(2)

            # page.on("dialog", lambda dialog: dialog.accept())
            # time.sleep(1)
            scroll_amount = random.randint(200, 800)  # Random scroll distance between 200px and 800px
            scroll_direction = random.choice([1, -1])  # Randomize scroll direction (1 for down, -1 for up)
            time.sleep(random.uniform(1, 3))
            
            try:
                target_lat_str = page.locator('div#title:has-text("Latitude")').locator(
                    'xpath=following-sibling::div[@id="value"]').text_content().strip()
                # time.sleep(random.uniform(1, 3))
                target_lon_str = page.locator('div#title:has-text("Longitude")').locator(
                    'xpath=following-sibling::div[@id="value"]').text_content().strip()

                time.sleep(random.uniform(1, 3))

                scroll_amount = random.randint(200, 900)  # Random scroll distance between 200px and 800px
                scroll_direction = random.choice([1, -1])
                page.mouse.click(x, y) 
                page.mouse.wheel(0, scroll_amount * scroll_direction)  # Scroll by a random amount in the chosen direction
                time.sleep(random.uniform(2, 4))  # Random delay between actions (2 to 4 seconds)

                # Parse latitude/longitude
                target_lat = float(target_lat_str)
                target_lon = float(target_lon_str)
                # time.sleep(random.uniform(1, 3))



                if is_within_radius(city_lat, city_lon, target_lat, target_lon):
                    print(f"C17 Registration {regs} is within 100 miles of Vadodara. LAT {target_lat} {target_lon} \n")
                    print(f"Initiating VoIP Call Alert for +91 9909471247 & +916354248126,  {datetime.now()} \n")
                    print(f"Triggering Buzzer Alert on ESP8266 Microprocessor\n")
                    response = VoiceResponse()
                    response.say(
                        f"Hello, this is a call from 2kwattz Flight Alert System. Indian Air Force's C17 with Registration {regs} "
                        f"is within 100 miles of Vadodara at Lat {target_lat} and Lon {target_lon}. Grab your camera now",
                        voice="alice"
                    )
                    
                    # for numbers in numbersToCall:
                    #     client.calls.create(
                    #     url="http://demo.twilio.com/docs/voice.xml",
                    #     to=numbers,
                    #     from_="+17756187371",
                    #     twiml=str(response)
                    #     )

                    client.calls.create(
                        url="http://demo.twilio.com/docs/voice.xml",
                        to="+916354248126",
                        from_="+17756187371",
                        twiml=str(response)
                    )
                    time.sleep(2)
                    client.calls.create(
                        url="http://demo.twilio.com/docs/voice.xml",
                        to="+919909471247",
                        from_="+17756187371",
                        twiml=str(response)
                    )

                    time.sleep(2)
                    client.calls.create(
                        url="http://demo.twilio.com/docs/voice.xml",
                        to="+919874867962",
                        from_="+17756187371",
                        twiml=str(response)
                    )


                    # 916354248126
                    time.sleep(5)
                    with data_lock:
                        print("Updating Web Socket Endpoints ...",datetime.now())
                        shared_dict[regs] = True

                        print("Values in web socket endpoint", shared_dict)
                else:
                    print(f"\n Registration {regs} is NOT within 100 miles of Vadodara. {datetime.now()}",)
                    print(f" {regs} LAT LONG {target_lat} {target_lon} . Vadodara's LAT LONG {city_lat} {city_lon},  {datetime.now()}")
                    # time.sleep(6)
                    with data_lock:
                        print("Updating Web Socket Endpoints ...")
                        shared_dict[regs] = False

                        # print("Values in shared dict", shared_dict)

            except Exception as e:
                print(f"Error with processing aircraft {regs}: {e}  {datetime.now()}")

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


            print("Error:  ",e)

            task_status["result"] = str(e)
        if "ERR" in task_status["result"] or "Timeout" in task_status["result"] or "Error" in task_status["status"]:
            print("ERR , TIMEOUT ERROR",task_status["result"])
            
            perform_check()

        # Sleep for 15 minutes (900 seconds) before running again

        random_interval = random.randint(min_interval,max_interval)
        print(f"Waiting for delay of {random_interval} seconds before sending next request")
        time.sleep(random_interval)

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





