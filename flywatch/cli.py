import asyncio
import random
import json
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async
import pytz
from datetime import datetime
import math
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import datetime


# --------------------------------------------
# Bot Evading Tactics
# --------------------------------------------

# Description:
# Anti Bot evading tactics are implemented to prevent anti bot mechanisms from detecting  
# our web scrapping so that we can know the aircraft movements every 15 minutes without 
# raising flags


# --------------------------------------------
# List of Accept headers to mimic real user behavior
# --------------------------------------------

# Description:
# The Accept header informs the server about the types of content that the client can handle. 
# This list includes 10 variations commonly used by real browsers to evade bot-detection mechanisms.
# Randomizing these headers helps simulate realistic requests during testing or scraping.

accept_headers = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.8,image/apng,image/webp,*/*;q=0.7",
    "text/html,application/xml;q=0.9,application/json,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.7,image/avif,image/webp,*/*;q=0.6",
    "text/html,application/json;q=0.9,image/webp,image/apng,*/*;q=0.5",
    "text/html,application/xhtml+xml;q=0.8,application/xml;q=0.6,image/webp,*/*;q=0.9",
    "text/html,application/xhtml+xml;q=0.7,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/json;q=0.8,application/xml;q=0.9,image/webp,*/*;q=0.6",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.7",
    "text/html,application/xhtml+xml;q=0.8,image/avif,image/webp,*/*;q=0.5"
]

selected_header = random.choice(accept_headers)

# --------------------------------------------
# User Agents Randomisation Data
# --------------------------------------------

# Description:
# User Agent randomisation is used to mask and vary the identity of requests made 
# to a server by simulating requests from different browsers or devices. This tactic 
# helps in preventing detection and blocking by server-side filters or security systems. 
# It ensures anonymity, evasion of detection mechanisms, and circumvents restrictions 
# based on known patterns of user agents.

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Android 10; SM-A505G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.73",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 12_5_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; SM-A526B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A716B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
]

# --------------------------------------------
# Fetching Current Month and Year
# --------------------------------------------

# Description:
# Fetching the current month and year for time modifier keyword for HTTP Header Referer
# which will create an impression of more 'natural' browsing keywords pattern in the HTTP Header's referer
# and Origin

today = datetime.datetime.now()
current_month_number = today.month
current_month_name = today.strftime("%B")  # Full month name
current_year = today.year


# --------------------------------------------
# Keyword Configuration Data
# --------------------------------------------

# Description:
# This section contains arrays of core keywords, intent modifiers, time modifiers, 
# and location-based keywords. These keywords are randomly combined to dynamically 
# generate search strings. This randomisation technique prevents predictable patterns, 
# making bot detection harder and improving query versatility by simulating varied 
# search behaviors and contexts.

core_keywords = ["C-17", "military aircraft", "aircraft", "Globemaster", "C17 Globemaster", "Jet", "Indian Air Force", "Flight", "IAF", "C17", "Transport Plane"]
intent_modifiers = ["registration", "tracking", "monitoring", "flightpath", "movements", "air traffic", "track", "airspace", "update"]
time_modifiers = ["this week", "today", "history", "last 24 hours", "recent", "yesterday", datetime.datetime.now().strftime("%B"), str(datetime.datetime.now().year), "24 hours"]
location_keywords = ["Near Me", "India", "Bharat", "Gujarat", "Asia", "Tamil Nadu", "Jammu", "Kashmir", "Ladakh", "Rajasthan", "Kerala", "United States", "US"]


# --------------------------------------------
# Referer URL Configuration Data
# --------------------------------------------

# Description:
# This section defines a list of referer objects containing search engine URLs and their respective domains. 
# These URLs are dynamically used to randomize search patterns and simulate searches from different 
# sources. This randomization enhances variability in query requests and helps evade detection by 
# mimicking legitimate user traffic originating from various popular search engines.

REFERER_OBJECTS = [
    {"url": "https://www.bing.com/search?q={query}", "domain": "https://www.bing.com"},
    {"url": "https://www.google.com/search?q={query}", "domain": "https://www.google.com"},
    {"url": "https://search.yahoo.com/search?p={query}", "domain": "https://search.yahoo.com"},
    {"url": "https://duckduckgo.com/?q={query}", "domain": "https://duckduckgo.com"},
    {"url": "https://www.ecosia.org/search?q={query}", "domain": "https://www.ecosia.org"},
]

def weighted_random_choice(array):
    """Helper for selecting random elements."""
    return random.choice(array)

# --------------------------------------------
# Generate Search Query for Http Header Referer
# --------------------------------------------

def generate_search_query():
    """
    Generates a dynamic search query based on random combinations of keywords.
    """
    core = weighted_random_choice(core_keywords)
    intent = weighted_random_choice(intent_modifiers)
    time = weighted_random_choice(time_modifiers)
    location = weighted_random_choice(location_keywords)

    # Create contextually valid combinations
    if random.random() > 0.5:
        # Case 1: Core + Intent + Time
        search_term = f"{core} {intent} {time}"
    else:
        # Case 2: Core + Intent + Location + Time
        search_term = f"{core} {intent} {location} {time}"

    # Sanitize/URL-encode query (basic encoding)
    search_term = search_term.replace(" ", "+")
    print(f"Generated Search Query: {search_term}")
    return search_term


# --------------------------------------------
# ASCII Header when the script starts up
# -------------------------------------------- 

def print_stylized_header():
    # Green border escape code
    GREEN = "\033[32m"
    RESET = "\033[0m"
    
    border = GREEN + "+" + "=" * 70 + "+" + RESET
    title = "🚀 C-17 Aircraft Movement Detection Script 🚀"
    author = "Code by Roshan Bhatia"
    ig_handle = "IG: @2kwattz"
    
    # Print the header with green border only
    print("\n")
    print(border)
    print(f"| {title.center(70)} |")
    print("|" + " " * 72 + "|")
    print(f"| {author.center(70)} |")
    print(f"| {ig_handle.center(70)} |")
    print(border)
    print("\n")


print_stylized_header()

def get_random_referer_and_origin():
    selected = random.choice(REFERER_OBJECTS)
    referer_url = selected["url"]  # URL for Referer
    origin_domain = selected["domain"]  # Domain for Origin

    print(f"Random HTTPS Header Referer & Origin Generated {referer_url} {origin_domain}.\n")
    print("Random User Agent String Generated\n")
    return referer_url, origin_domain

# HTTPS Headers for Scrapping request



def generateHeaders():
       
       referer, origin = get_random_referer_and_origin()
       query = generate_search_query()
       selected_referer_template = random.choice(REFERER_OBJECTS)
       referer_url = selected_referer_template["url"].replace("{query}", query)
       HEADERS = {
        "User-Agent": random.choice(USER_AGENTS), # Randomize User-Agent
        "Referer": referer_url,  # Randomize the Referer
        # "Accept-Language":  # Coz I need english
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-AU,en;q=0.7"]),
        "DNT": str(random.choice([0,1])), # DNT Really Doesnt matter
        "Upgrade-Insecure-Requests": str(random.choice([0,1])),
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Origin": origin,
        "Accept": selected_header
    }
       
       print("Dynamic Headers", HEADERS)
       return HEADERS

generateHeaders()


