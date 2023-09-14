from tkinter import *
#from PIL import Image, ImageTk
from queue import Queue
from mutagen.mp3 import MP3
import pygame
import csv
import os
from tkinter import filedialog
root = Tk()
root.title('LED-Pattern')
root.iconbitmap("images/Icon2.ico")
root.geometry("1000x500")
root.resizable(False, False)

ControlFrame = Frame(root)
ControlFrame.place(x=310, y=420)
playButton = Button(ControlFrame, text="Play", font=("Helvetica", 16), command=lambda: helper(Flag))
statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
customizeButton = Button(ControlFrame, text="Customize!", command=lambda: customize(paused, Flag),
                         font=("Helvetica", 16))
finish_button = Button(ControlFrame,text="Finish",font=("Helvetica", 16), command=lambda: [create_and_saveCsv(csvCounter),root.destroy()])

# playButton.place(x=300,y=450)
playButton.grid(row=0, column=0)
finish_button.grid(row=0,column=5)

pauseButton = Button(ControlFrame, text="Pause", command=lambda: pause(paused), font=("Helvetica", 16))
pauseButton.grid(row=0, column=1)
restartButton = Button(ControlFrame, text="Restart", command=lambda: Restart(paused, Flag), font=("Helvetica", 16))
restartButton.grid(row=0, column=2)

customizeButton.grid(row=0, column=3)

statusBar.pack(fill=X, side=BOTTOM, ipady=2)

my_menu = Menu(root)
root.config(menu=my_menu)
Song_menu=Menu(my_menu)
my_menu.add_cascade(label="Add songs!!",menu=Song_menu)

song_box = Listbox(root,bg = "white",fg = "black",width = 60,height = 2)
song_box.place(x=0,y=0)
frame_grid = Frame(root)
frame_grid.place(x = 0,y = 80)
frames = []
for i in range(8):
    frame = Frame(frame_grid)
    frame.grid(row=i // 4, column=i % 4, padx=20, pady=10)
    frames.append(frame)

# Create buttons in each frame labeled from 1 to 8
for i in range(8):
    counter = 1
    for row in range(4):
        for col in range(2):
            button_label = row * 4 + col + 1
            button = Button(frames[i], text="LED# "+str(counter))
            counter+=1
            button.grid(row=row, column=col, padx=5, pady=5)



root.mainloop()