# --------------------FINDMYFLIX--------------------
#
# Developed by Ryan Harding 2022
# Released under GNU Public License (GPL)
# Contact: rn.hardingg@utexas.edu, rnharding.com
#
#---------------------------------------------------

import os, sys
import requests
import json
from PIL import Image, ImageTk
from io import BytesIO
import config

# Helper class used to organize information for detailed view of a result
class ShowCard:
    def __init__(self, id, title, image, type):
        # Make request and save result
        req = "https://api.watchmode.com/v1/title/" + str(id) + "/details/?apiKey=" +\
               config.key + "&append_to_response=sources"
        result = requests.get(req)
        j = json.loads(result.text)
        
       ### Uncomment below and comment above for debugging/testing ###
	   ### Uses breakingbadshow.json as offline detail test data to avoid request spam ###

        # j = json.load(open(r'tests\breakingbadshow.json'))
        
        self.title = title
        self.img = image
        self.type = type

        # Parse json object for detailed information
        self.blurb = "Blurb not available" if not j['plot_overview'] else j['plot_overview']
        self.release_year = type + ": " 
        self.release_year += "N/A" if not j['year'] or j['year'] == "" else str(j['year'])
        self.release_date = "N/A" if not j['release_date'] or j['release_date'] == "" else j['release_date'] 
        self.end_year = "N/A" if not j['end_year'] or j['end_year'] == "" else j['end_year']
        self.runtime_mins = "N/A" if not j['runtime_minutes'] or j['runtime_minutes'] == "" else j['runtime_minutes']
        self.genres = []
        for genre in j['genre_names']:
            self.genres.append(genre)
        self.audience_score = "N/A" if not j['user_rating'] or j['user_rating'] == "" else int(j['user_rating'] * 10)
        self.critic_score = "N/A" if not j['critic_score'] or j['critic_score'] == "" else j['critic_score']
        self.age_rating = "N/A" if not j['us_rating'] or j['us_rating'] == "" else j['us_rating']
        self.trailer_link = "N/A" if not j['trailer'] or j['trailer'] == "" else j['trailer']
        
        # Collect sources for this show
        self.sources = []
        source_ids = []
        for source in j['sources']:
            if (source['source_id'] not in source_ids):
                cur_source = Source(source)
                self.sources.append(cur_source)
                source_ids.append(source['source_id'])
class Source:
    def __init__(self, s_json):
        self.name = s_json['name']
        img_result = logo_binary_search(s_json['source_id'])
        self.img = img_result
        self.url = "N/A" if not s_json['web_url'] or s_json['web_url'] == "" else s_json['web_url']

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Local file of all supported streaming sources, do not change
sources_path = resource_path("tests")
sources = json.load(open(sources_path + "\sources.json"))

# Binary searches sources.json for logo URL corresponding with ID
# Valid sources & links will return correct logo, otherwise returns no_logo.jpg
def logo_binary_search(tgt):
    low = 0
    high = len(sources) - 1
    mid = 0
    while low <= high:
        mid = (low + high) // 2
        if (sources[mid]['id'] < tgt):
            low = mid + 1
        elif (sources[mid]['id'] > tgt):
            high = mid - 1
        else:
            # Found source in sources.json, now need to check logo link
            if not sources[mid]['logo_100px'] or sources[mid]['logo_100px'] == "":
                assets_path = resource_path("assets")
                no_logo = ImageTk.PhotoImage(Image.open(assets_path + r'\no_logo.jpg'))
                return no_logo
            else:
                response = requests.get(sources[mid]['logo_100px'])
                img_data = response.content
                logo = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
                return logo