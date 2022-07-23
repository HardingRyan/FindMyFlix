# --------------------FINDMYFLIX--------------------
#
# Developed by Ryan Harding 2022
# Released under GNU Public License (GPL)
# Contact: rn.hardingg@utexas.edu, rnharding.com
#
#---------------------------------------------------

import requests
from PIL import Image, ImageTk
from io import BytesIO
import os, sys

# Helper class used to organize information related to a specific search result.
class ResultCard:
    def __init__(self, title, type, year, img_url, id) -> None:
        self.title = title
        self.id = id
        if not type or type == "":
            self.type = "UNKNOWN TYPE"
        elif type == "tv_series":
            self.type = "TV Series"
        elif type == "short_film":
            self.type = "Short Film"
        elif type == "tv_miniseries":
            self.type = "TV Mini-Series"
        else:
            self.type = "Movie"
        
        self.year = "UNKNOWN YEAR" if not year or year == "" else year

        if not img_url or img_url == "https://cdn.watchmode.com/profiles/":
            assets_path = resource_path("assets")
            self.img = ImageTk.PhotoImage(Image.open(assets_path + "\error.jpg"))
        else:
            response = requests.get(img_url)
            img_data = response.content
            img_result = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            self.img = img_result

    # Debugging Helper Method
    def print(self):
        print(self.name)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)