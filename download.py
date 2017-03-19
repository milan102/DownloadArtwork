import urllib.request
import os
import datetime
import tkinter.messagebox


def download_image(event, url):
    # Current date as a string
    current_date = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    # Part that comes after the last slash in the URL
    last_part_of_url = url.split('/')[-1]
    picture_name = last_part_of_url.split('.')[0]
    file_extension = last_part_of_url.split('.')[-1]
    complete_filename = picture_name + '.' + file_extension[0:3]

    # Save location, add date to the filename
    save_location = os.path.expanduser("~") + "\\Desktop"
    final_file_name = os.path.join(save_location, current_date + "_" + complete_filename)

    # Retrieves image for download, throws exception as a message box if an error is found
    try:
        urllib.request.urlretrieve(url, final_file_name)
        tkinter.messagebox._show('SUCCESS', complete_filename + '\nhas been downloaded to your desktop.')
    except Exception as e:
        tkinter.messagebox.showerror('ERROR', str(e) + '\n\nPick a different image.')