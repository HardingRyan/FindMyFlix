import requests
from PIL import Image, ImageTk
from io import BytesIO


class ResultCard:
    def __init__(self, title, type, year, img_url, id) -> None:
        self.title = title
        self.id = id
        
        #TODO maybe see if it is possible to make enum for types?
        #or an algo to maybe parse the raw types into theses versions idk
        # https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
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
            self.img = ImageTk.PhotoImage(Image.open("assets\error.jpg"))
        else:
            response = requests.get(img_url)
            img_data = response.content
            img_result = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            self.img = img_result

        
    
    def print(self):
        print(self.name)