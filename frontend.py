import tkinter as tk
from PIL import Image, ImageTk
import backend as bck 
from tkinter import messagebox
import threading

#command for button 
def submit():
    final_username = username_entry.get()
    final_client_secret = client_secret_entry.get()
    final_genre = clicked.get().lower()
    final_number_of_songs = int(number_of_songs_entry.get())
    final_playlist_name = playlist_name.get()
    final_description = playlist_description.get("1.0", 'end-1c')
    final_privacy = clicked1.get().lower()
    if(final_number_of_songs > 100):
        messagebox.showinfo("", "Try again. Max songs is 100.")
    else:
        threading.Thread(target=bck.backend(final_username, final_client_secret, final_genre, final_number_of_songs, final_playlist_name, final_description, final_privacy)).start()
        messagebox.showinfo("", "Complete!")

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=600)
canvas.grid(columnspan=3, rowspan=3)

#logo 
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#username
tk.Label(root, text="Username", font='Raleway').place(x=50, y=280)
username_entry= tk.Entry(root, bd=2)
username_entry.place(x=150, y=286)

#client secret 
tk.Label(root, text="Client Secret", font='Raleway').place(x=50, y=305)
client_secret_entry= tk.Entry(root, bd=2)
client_secret_entry.place(x=173, y=310)

#genre 
clicked = tk.StringVar()
clicked.set("")
tk.Label(root, text="Genre", font='Raleway').place(x=435, y=305)
tk.OptionMenu(root, clicked, "Pop", "Rap", "EDM", "Country", "Rock", "Indie", "Folk").place(x=500, y=305)

#number of songs 
tk.Label(root, text="Number of Songs", font='Raleway').place(x=340, y=277)
number_of_songs_entry= tk.Entry(root, bd=2, width=5)
number_of_songs_entry.place(x=500, y=283)

#playlist name 
tk.Label(root, text="Playlist Name", font='Raleway').place(x=105, y=350)
playlist_name= tk.Entry(root, bd=2)
playlist_name.place(x=235, y=355)

#playlist description 
tk.Label(root, text="Description", font='Raleway').place(x=125, y=375)
playlist_description= tk.Text(root, bd=2, height=6, width=40)
playlist_description.place(x=235, y= 380)

#privacy 
clicked1 = tk.StringVar()
clicked1.set("")
tk.Label(root, text="Privacy", font='Raleway').place(x=155, y=480)
tk.OptionMenu(root, clicked1, "Public", "Private").place(x=230, y=480)

canvas = tk.Canvas(root, width=600, height=450)
canvas.grid(columnspan=3)

#description
tk.Label(root, text="Create your Spotify Playlist", font='Raleway').place(x=185, y=515)

#submit button
submit_text = tk.StringVar()
tk.Button(root, textvariable=submit_text, command=submit, font="Raleway", bg='#1DB954', fg='white', height=2, width=15).place(x=225, y=550)
submit_text.set('Submit')

root.mainloop()