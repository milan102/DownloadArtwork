from googleapiclient.discovery import build
import tkinter as tk
from PIL import ImageTk
from io import BytesIO
from urllib.request import Request, urlopen
from tkinter import *
from PIL import Image
from download import download_image
import ssl

# Initialize service w/ a custom search engine that uses dev key
# Set your developer key
service = build("customsearch", "v1",
                developerKey="")


def search_results():
    # Query, custom search engine ID, number of results
    # Set your custom search engine id in cx
    results = service.cse().list(
        q=getText(),
        cx='',
        searchType='image',
        num=8,
        safe='off'
    ).execute()

    # Get rid of initial GUI
    master.destroy()

    # Empty url list
    urls = []

    # Add items from results to url list
    for item in results['items']:
        urls.append(item['link'])

    # Call function to display results
    show_pictures(urls)


def show_pictures(urls):
    # Picture display's GUI settings
    root = tk.Tk()
    root.resizable(width=False, height=False)
    rows = 0
    columns = 0
    MAX_NUMBER_OF_COLUMNS = 4

    for url in urls:
        # Browser settings
        user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        req = Request(url, headers={'User-Agent': user_agent})
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        context = ssl._create_unverified_context()

        # Attempt to open url to check if valid
        try:
            u = urlopen(req, context=context)
        except Exception as e:
            print(e)
            continue

        # Grab data from url
        raw_data = u.read()
        u.close()
        image_file = Image.open(BytesIO(raw_data))
        image_file = image_file.resize((400, 400), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image_file)

        # Set labels to have images, and attach event to download image when clicked
        label = tk.Label(image=photo_image)
        label.image = photo_image
        label.grid(row=rows, column=columns)
        label.bind("<Button-1>", lambda event, image_link=url: download_image(event, image_link))

        # Increase columns until max columns are reached, and then columns are reset and a new row is added
        columns += 1
        if columns == MAX_NUMBER_OF_COLUMNS:
            rows += 1
            columns = 0

    root.mainloop()


# Return entry text
def getText():
    return textbox1.get()


# Delete entry text
def clear_text_box(event, text):
    text.set("")

# Infinite loop that allows the search box GUI to keep appearing over and over again, until it is closed
while True:
    master = Tk()

    initialText = StringVar(None)
    initialText.set("Type your search query here")

    textbox1 = Entry(master, textvariable=initialText, width=100)
    textbox1.bind("<Button-1>", lambda event, to_clear=initialText: clear_text_box(event, to_clear))
    textbox1.grid(row=0, column=1, padx=4)

    Button(master, text='Search', command=search_results).grid(row=0, column=2, sticky=W, padx=2, pady=2)

    master.protocol("WM_DELETE_WINDOW", quit)
    master.mainloop()



