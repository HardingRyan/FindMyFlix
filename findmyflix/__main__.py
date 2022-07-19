# --------------------FINDMYFLIX--------------------
#
#			 Developed by Ryan Harding 2022
#
#---------------------------------------------------

import json
import requests
import urllib.parse
import webbrowser
 #TODO maybe only do the individual imports?
 #from tkinter import *
from tkinter import Tk, END, RIGHT, Y, HORIZONTAL, ttk, Frame, Label, LabelFrame, Button, Text, Entry
from tkinter import ttk
from PIL import Image, ImageTk
from resultcard import ResultCard
from showcard import *
from functools import partial
from tkHyperlinkManager import HyperlinkManager
import config

root = Tk()
root.title('FindMyFlix')
root.iconbitmap('assets\logo.ico')
root.geometry("1050x700")
root.minsize(1050, 700)
root.configure(bg='#000')

# Constants
font_family = "Segoe UI"
global images
images = []
boxes = []
temp_img = Image.open("assets/mfbackground.jpg")
temp_img_copy = temp_img.copy()
background_image = ImageTk.PhotoImage(temp_img)

style=ttk.Style()
style.theme_use('clam')
style.configure("Horizontal.TProgressbar", background="#802223", bd=0)
style.configure("Vertical.TScrollbar", background="#802223", arrowsize=40, gripcount=0, borderwidth=0, relief="groove", troughcolor="#000")

# Dynamically positions all elements based on current window size
def resize(e):
	welcome.place(relx = .5, y = 75, anchor="center")
	blurb.place(relx = .5, y = 150, anchor="center")
	prompt.place(relx = .1, y = 195)
	entry_box.place(relx = .1, y = 230, relwidth=.65)
	search_button.place(relx = .8, y = 225)
	clear_button.place(relx = .9, y = 225)
	misc_info.place(relx=.5, y=280, anchor="center")
	results_frame.place(relx = .5, rely = 1, relheight = .5, relwidth = 1, anchor = "s")
	temp_img = temp_img_copy.resize((results_frame.winfo_width(), results_frame.winfo_height()))
	background_image = ImageTk.PhotoImage(temp_img)
	bg.configure(image = background_image)
	bg.image = background_image
	bg.pack()
	results_box.place(relheight=1, relwidth=1, relx=1, rely=1, anchor="se")

# Queries API for relevant titles regarding entry_box text value
def search():
	progress_bar.place(relx = .5, y = 310, anchor="center", relwidth=.5)
	movieName = str(urllib.parse.quote(entry_box.get()))
	clear()
	# TEMPORARILY DISABLED REQUESTING FOR TESTING
	#TODO I have the search mode for titles only, what about people too? idk maybe another feature
	# req = "https://api.watchmode.com/v1/autocomplete-search/?apiKey=" + config.key + "&search_value=" + movieName + "&search_type=2"
	# result = requests.get(req)
	# result_json = json.loads(result.text)
	# print(result_json)

	### UNCOMMENT BELOW FOR DEBUGGING, COMMENT ABOVE ###

	result_json = json.load(open(r'.\tests\breakingbad.json'))


	fill_results(result_json)

# Dynamically creates and allocates search results to display box	
def fill_results(json_data):
	cards_loaded = 0
	for obj in json_data['results']:
		progress_bar['value'] = cards_loaded / len(json_data['results']) * 100
		curCard = ResultCard(obj['name'], obj['type'], obj['year'], obj['image_url'], obj['id'])
		
		curBox = Frame(results_frame, relief="groove", background="gray",
                       width=500, height=330, bd=5, cursor = 'arrow white')
		curBox.pack(fill = None, expand = False)
		boxes.append(curBox)
		results_box.configure(state="normal")
		results_box.window_create("end", window=curBox)
		results_box.configure(state="disabled")

		# Loading display values
		image = Label(curBox, image=curCard.img, bd='0')
		image.place(anchor='nw')
		images.append(curCard.img)

		title_and_info = curCard.title + "\n" + (str)(curCard.year) + " - " + curCard.type
		title = Label(curBox, text=title_and_info, bg="gray", fg="white",
					  bd="0", font=(font_family, '15', 'bold'))
		title.config(wraplength="290")
		title.place(x = 350, anchor="n")

		details_button = Button(curBox, text="View Details", bg="#802223", fg="#fff", font=(font_family, 15), command=partial(view_details, curCard.id, curCard.title, curCard.img, curCard.type))
		details_button.place(x = 350, y = 200, anchor="n")
		root.update_idletasks()
		cards_loaded += 1 
	
	progress_bar.place_forget()
	progress_bar['value'] = 0
	vert_scroll.pack(side = RIGHT, fill = Y)


# Creates wide card with more specific information about selected media
def view_details(id, title, image, type):
	show_card = ShowCard(id, title, image, type)
	d_frame = Frame(results_frame, relief="groove", background="gray",
                       width=1000, height=350, bd=5, cursor = 'arrow white')
	d_frame.pack(fill = None, expand = False)
	boxes.append(d_frame)
	
	d_img = Label(d_frame, image=show_card.img, bd=0)
	d_img.place(anchor='w', y = 175)

	d_title_frame = Frame(d_frame, bg='gray', bd=0, cursor='arrow white', width=870, height=35)
	d_title = Text(d_title_frame, bg='gray', fg='#fff', bd=0.5, wrap="word", font=(font_family, 22, 'bold'), padx=0, pady=0, cursor='arrow white')
	d_title.tag_configure("center", justify='center')
	d_title.insert('0.0', show_card.title)
	d_title.tag_add("center", '0.0', 'end')
	d_title['state'] = 'disabled'
	d_title_frame.place(x=470, anchor='n')
	d_title.place(relheight=1, relwidth=1, relx=1, rely=1, anchor='se')

	d_close_btn = Button(d_frame, text="Close", bg="#802223", fg='#fff', font=(font_family, 15), command=partial(close_details_window, d_frame))
	d_close_btn.place(x = 995, anchor="ne")

	# Blurb
	b_frame = Frame(d_frame, bg="gray", bd='0', width = 500, height = 65, cursor = 'arrow white')
	d_blurb = Text(b_frame, wrap="word", bg="gray", fg='#fff', cursor = 'arrow white', bd='1', font=(font_family, 10))
	b_frame.place(x = 735, y = 120, anchor="s")
	d_blurb.place(relheight=1, relwidth=1, relx=1, rely=1, anchor="se")
	d_blurb.insert(0.0, show_card.blurb)
	d_blurb.config(state="disabled")

	# Misc Info
	m_box = Text(d_frame, bg="gray", fg='#fff', bd=1, cursor='arrow white', wrap="word", font=(font_family, 14))
	m_box.place(x=300, y = 320, width=220, height=270, anchor="s")
	m_box.insert(0.0, show_card.release_year)
	if (not show_card.type in ("Movie", "Short Film")):
		m_box.insert(END, "-" + str(show_card.end_year))
		m_box.insert(END, "\nAverage Episode: " + str(show_card.runtime_mins) + " mins")
	else:
		m_box.insert(END, "\nRuntime: " + str(show_card.runtime_mins) + " mins")
	m_box.insert(END, "\nGenres: ")
	for genre in show_card.genres:
		m_box.insert(END, genre)
		if (not genre == show_card.genres[-1]):
			m_box.insert(END, ", ")
	m_box.insert(END, "\n\n")
	m_box.insert(END, "Audience Rating: " + str(show_card.audience_score) + "%")
	m_box.insert(END, "\nCritic Rating: " + str(show_card.critic_score) + "%\n\n")

	# Ratings & Trailer
	m_box.insert(END, "Age Rating: " + show_card.age_rating)
	m_box.tag_add("audience_color", '5.17', '5.20')
	m_box.tag_configure("audience_color", foreground=get_color(show_card.audience_score), font=(font_family, 15, 'bold'))
	m_box.insert(END, "\nTrailer: ")
	m_box.tag_add("critic_color", '6.15', '6.18')
	m_box.tag_configure("critic_color", foreground=get_color(show_card.critic_score), font=(font_family, 15, 'bold'))
	if show_card.trailer_link == "N/A":
		m_box.insert(END, "N/A")
	else:
		trailer_link = HyperlinkManager(m_box)
		m_box.insert(END, "Here", trailer_link.add(partial(webbrowser.open, show_card.trailer_link)))
	
	# Streaming sources
	s_frame = LabelFrame(d_frame, text="Where To Watch:", labelanchor='n', bg="gray", fg='#fff', bd='1', width=500, height=180, font=(font_family, '12'))
	s_box = Text(s_frame, wrap="word", bg='gray', fg='#fff', cursor='arrow white', state='disabled', font=(font_family, 13))
	s_frame.place(x = 735, y = 140, anchor='n')
	s_box.place(relheight=1, relwidth=1, relx=1, rely=1, anchor='se')

	s_box.config(state="normal")
	#TODO progress bar for loading source cards?
	#I think the labor intensive part is the SHowCard() constructor
	#How to get a progress bar on that? maybe reuse the same one
	for source in show_card.sources:
		cur_source_box = Frame(s_frame, relief="groove", background="gray", width=100, height=135, bd=1, cursor="arrow white")
		cur_source_box.pack(fill = None, expand = False)
		
		s_box.window_create("end", window=cur_source_box)
		
		
		cur_source_logo = Label(cur_source_box, image=source.img, bd=1)
		cur_source_logo.place(anchor='nw')
		images.append(source.img)

		if (source.url != "N/A"):
			cur_source_link = Label(cur_source_box, text=source.name, fg='blue', bg='gray', bd=0, cursor='hand2', font=(font_family, 11, 'underline'))
			cur_source_link.place(y=117, anchor='center', relx=.5)
			cur_source_link.bind("<Button-1>", lambda e, l = source.url: webbrowser.open(l))
		else:
			cur_source_link = Label(cur_source_box, text=source.name, bg='gray', bd=0, cursor='hand2', font=(font_family, 11))
			cur_source_link.place(y=117, anchor='center', relx=.5)
	s_box.config(state="disabled")	


# Returns correct color based on audience/critic rating for details card
def get_color(score):
	if (score == "N/A"):
		return "white"
	elif (0 <= score <= 49):
		return "#cc0000"
	elif (50 <= score <= 64):
		return "#e69138"
	elif (65 <= score <= 79):
		return "#f1c232"
	elif (80 <= score <= 89):
		return "#93c47d"
	else:
		return "#38761d"
	
# Wipes search results area
def clear():
	for box in boxes:
		box.destroy()
	entry_box.delete(0, END)
	images.clear()
	boxes.clear()
	vert_scroll.pack_forget()

def close_details_window(d_frame):
	d_frame.destroy()


# Initialize template elements
welcome = Label(root, text = "Welcome!", fg="#fff", bg="#000", font=(font_family, '50', 'bold'))
blurb = Label(root, text = "Enter a movie/TV show name to query over 200 streaming platforms.", fg="#fff", bg="#000", font=(font_family, '20'))
prompt = Label(root, text = "What movie/show are you looking for?", fg="#fff", bg="#000", bd="0", font=(font_family, '15'))
entry_box = Entry(root, font=(font_family, 18), width = 50)
search_button = Button(root, text="Search", font=(font_family, 15), fg="#fff", bg="#802223", command = search)
clear_button = Button(root, text ="Clear", font=(font_family, 15), fg="#fff", bg="#802223", command = clear)

#TODO maybe how to put an email hyperlink?
#also when project page is made at rnharding.com/blog/findmyflix, link that
#in order to do this i might have to change this label to a small text box with disabled status
misc_info = Label(root, text = "Developed by Ryan Harding, 2022. Direct any bug reports, comments, or questions to rn.hardingg@utexas.edu. Project webpage [HERE].", anchor="center", fg="#fff", bg="#000", font=(font_family, 8), bd=0)
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate')

# Results Box
results_frame = Frame(root, bg="#000")
results_box = Text(results_frame, wrap="char", height="20", width="60", bg = "#000", fg="#fff", bd="0", state="disabled", cursor='arrow white')
bg = Label(results_box, image=background_image)
#TODO the scrolling only works when the cursor is physically on the scrollbar, this isnt the case in normal Scrollbar where its anywhere that isnt covered by a result card
#would it be possible to enable scrolling anywhere within the results frame?
vert_scroll = ttk.Scrollbar(results_frame, orient='vertical', command=results_box.yview, style="Vertical.TScrollbar")
results_box['yscrollcommand'] = vert_scroll.set


root.bind("<Return>", lambda e: search())
root.bind("<Configure>", resize)
root.mainloop()