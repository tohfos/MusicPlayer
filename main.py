import time
import threading

from tkinter import *
# from PIL import Image, ImageTk
from queue import Queue
from mutagen.mp3 import MP3
import pygame
import csv
import os
import tkinter.ttk as ttk
import concurrent.futures
from tkinter import filedialog
from customization import Customization
from tkinter import messagebox


class Customization:
    _timestamp = 0
    command = "0000000000000000000000000000000000000000000000000000000000000000"
    character_num = 0

    def __init__(self, character_num, _timestamp, command):
        self._timestamp = _timestamp
        self.command = command
        self.character_num = character_num

    def print_data(self):
        list = [self.command, self._timestamp, self.character_num]
        return list

    def get_timestamp(self):
        return self._timestamp

    def get_command(self):
        return self.command

    def set_command(self, new_command):
        self.command = new_command

    def get_character_num(self):
        return self.character_num

    def set_character_num(self, character_num):
        self.character_num = character_num


customization_list = []
stored_timestamps = []
spare_display_timestamps = []

root = Tk()
root.title('LED-Pattern')
root.iconbitmap("images/Icon2.ico")
root.geometry("1000x550")
root.resizable(False, False)

pygame.mixer.init()

global paused
paused = False
global Flag
Flag = False
global csvCounter
csvCounter = 0

my_menu = Menu(root)
root.config(menu=my_menu)
Song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs!!", menu=Song_menu)


def read_csv_and_add_to_list(song_name):
    csv_filepath = 'commands/routine'

    if not os.path.exists(csv_filepath):
        return False
    else:
        with open(csv_filepath, 'r') as csv_filepath:
            csv_reader = csv.reader(csv_filepath)
            for row in csv_reader:
                custom = Customization(0,float(row[1]),row[0])
                customization_list.append(custom)

def add_song():
    song = filedialog.askopenfilename(initialdir='Songs', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace(r"C:/Users/ahmed/MusicPlayer-remade/Songs/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)


Song_menu.add_command(label="Add Song", command=add_song)

song_box = Listbox(root, bg="white", fg="black", width=60, height=2)
song_box.place(x=0, y=0)


def helper(helperFlag):
    global Flag
    Flag = helperFlag
    play(Flag)


ControlFrame = Frame(root)
ControlFrame.place(x=360, y=470)
playButton = Button(ControlFrame, text="Play", font=("Helvetica", 16), command=lambda: helper(Flag))
statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
customizeButton = Button(ControlFrame, text="Customize!", command=lambda: customize(paused, Flag),
                         font=("Helvetica", 16))
finish_button = Button(ControlFrame, text="Finish", font=("Helvetica", 16),
                       command=lambda: [create_and_saveCsv(csvCounter), root.destroy()])

# playButton.place(x=300,y=450)
playButton.grid(row=0, column=1)
finish_button.grid(row=0, column=4)

pauseButton = Button(ControlFrame, text="Pause", command=lambda: pause(paused), font=("Helvetica", 16))
pauseButton.grid(row=0, column=2)
restartButton = Button(ControlFrame, text="Restart", command=lambda: Restart(paused, Flag), font=("Helvetica", 16))
restartButton.grid(row=0, column=5)

customizeButton.grid(row=0, column=3)

# pauseButton.place(x=360,y=450)


statusBar.pack(fill=X, side=BOTTOM, ipady=2)


def show_Leds(command):
    print("entered show leds")
    current_time = pygame.mixer_music.get_pos() / 1000

    frame_grid = Frame(root)
    frame_grid.place(x=100, y=80)
    frames = []
    command_list = []
    for i in range(8):
        frame = Frame(frame_grid)
        frame.grid(row=i // 4, column=i % 4, padx=20, pady=10)

        frames.append(frame)

    # Create buttons in each frame labeled from 1 to 8
    previous_flag = False
    for i in range(8):
        button_counter = 1
        helpVar = 0

        for row in range(4):
            for col in range(2):

                button = Button(frames[i], text="LED# " + str(button_counter) + "@" + str(i + 1))

                customization_command_string = command
                chunk_size = 8
                bit_chunks_customization = [customization_command_string[i:i + chunk_size] for i in
                                            range(0, len(customization_command_string), chunk_size)]
                current_command = bit_chunks_customization[i]

                res = light_helper(current_command, row, col)

                index_to_light = res[0]

                if "1" in current_command:
                    for index in range(len(index_to_light)):
                        if index_to_light[index] == button_counter - 1:
                            button.config(bg="yellow")

                button.grid(row=row, column=col, padx=5, pady=5)

                helpVar += 1
                button_counter += 1
    return True


def play_time():
    # Get Elapsed time
    print("current song postion ", pygame.mixer.music.get_pos())
    current_time = pygame.mixer.music.get_pos() / 1000
    print("current time", current_time)
    print("slider val ", my_slider.get())
    if my_slider.get() == 0:
        show_Leds("0000000000000000000000000000000000000000000000000000000000000000")

    if not paused:
        for customization in customization_list:
            if round(customization.get_timestamp(),3) == round(my_slider.get(),3):
                #print("showing leds at", round(my_slider.get(), 2))
                show_Leds(customization.get_command())


                #time.sleep(0.3)
                # time.sleep(0.2)

    # current time mohem gedan when iterating over the list, it is the time that gets saved in the timestamp

    slider_label.config(text=f'Slider: {(my_slider.get() - 0.05)} and Song Pos: {(current_time)}')

    current_time += 0.05  # Add 50 milliseconds (0.05 seconds)

    minutes, seconds = divmod(current_time, 60)
    seconds, milliseconds = divmod(seconds, 1)

    # Convert to formatted string
    converted_currentTime = f'{int(minutes):02}:{int(seconds):02}.{int((milliseconds * 1000) + 50):03}'

    # Get the currently selected song
    song = song_box.get(ACTIVE)
    song_path = f'C:/Users/ahmed/MusicPlayer-remade/Songs/{song}.mp3'
    song_mut = MP3(song_path)
    global song_length
    song_length = song_mut.info.length

    # Convert the song length to formatted string
    minutes, seconds = divmod(song_length, 60)
    seconds, milliseconds = divmod(seconds, 1)
    converted_SongLen = f'{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 1000):03}'

    if not paused:
        if round(my_slider.get() + 0.05, 1) == round(song_length, 1):
            statusBar.config(text=f'Time Elapsed: {converted_SongLen}')

        elif round(my_slider.get() + 0.05, 1) == round(current_time, 1):
            # slider didnt change on command
            slider_position = song_length

            my_slider.config(to=slider_position, value=current_time)
            statusBar.config(text=f'Time Elapsed: {converted_currentTime} of {converted_SongLen}')

        else:
            # slider changed position

            slider_position = song_length
            my_slider.config(to=slider_position, value=my_slider.get())
            helper = my_slider.get()

            minutes, seconds = divmod(helper, 60)
            seconds, milliseconds = divmod(seconds, 1)
            # Convert to formatted string
            newconverted_currentTime = f'{int(minutes):02}:{int(seconds):02}.{(int(milliseconds * 1000) + 50):03}'

            statusBar.config(text=f'Time Elapsed: {newconverted_currentTime} of {converted_SongLen}')
            # move along
            next_time = my_slider.get() + 0.05

            my_slider.config(value=next_time)
            if my_slider.get() == 0.0:
                pygame.mixer.music.set_pos(0)

                # time.sleep(0.5)

    # Update the status bar with elapsed time and song length

    # Schedule the function to run again after 50 ms (50 milliseconds)

    statusBar.after(50, play_time)

    return converted_currentTime


def play(PlayFlag, Restart_Flag=""):
    # show_Leds("0000000000000000000000000000000000000000000000000000000000000000")
    song = song_box.get(ACTIVE)
    song = f'C:/Users/ahmed/MusicPlayer-remade/Songs/{song}.mp3'
    read_csv_and_add_to_list(song)

    global csvCounter
    csvCounters = csvCounter
    global Flag
    Flag = PlayFlag
    # if PlayFlag:
    #     return
    if Restart_Flag == "restart_clicked":
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #pygame.mixer.music.rewind()
    else:
        try:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            Flag = True
            my_slider.config(state='enabled')
            if not PlayFlag:
                play_time()

            playButton.config(bg='cyan')
        except:
            messagebox.showerror(title="Song missing", message="Please add a song")


    csvCounter += 1

    # slider_position = int(song_length)
    # my_slider.config(to=slider_position,value=0)


def create_and_saveCsv(csvCount):
    global csvCounter
    csvCount=csvCounter
    list_of_data = []
    csvCounter+=1
    for custom in customization_list:
        data=[]
        data.append(custom.get_command())
        data.append(custom.get_timestamp())

        list_of_data.append(data)

    with open(r"C:\Users\ahmed\MusicPlayer-remade\commands\routine",mode='w',newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in list_of_data:
            writer.writerow(row)
def pause(is_paused):
    # TODO obtain timestamps when paused

    if Flag:
        global paused
        paused = is_paused
        if paused:
            pauseButton.config(text="Pause")
            my_slider.config(state="enabled")
            pygame.mixer.music.unpause()

            paused = False
        elif not paused:
            pauseButton.config(text="Resume")
            my_slider.config(state="disabled")

            pygame.mixer.music.pause()
            paused = True


def Restart(is_paused, helperFlag):
    print("restart clicked")
    global paused
    paused = is_paused
    paused=False

    global Flag
    Flag = helperFlag
    #pygame.mixer.music.stop()
    pygame.mixer.music.rewind()
    my_slider.config(value=0)

    #play(Flag, "restart_clicked")


def slide(x):
    # slider_label.config(text =f'{int(my_slider.get())} of {int(song_length)}' )
    song = song_box.get(ACTIVE)
    song = f'C:/Users/ahmed/MusicPlayer-remade/Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


def fetch_command_for_character(index, timestamp):
    for i in range(len(customization_list)):

        if customization_list[i].get_timestamp() == timestamp:
            command = customization_list[i].get_command()
            chunk_size = 8
            bit_chunks = [command[i:i + chunk_size] for i in range(0, len(command), chunk_size)]

            return bit_chunks[index]
    return False


def fetch_command(timestamp, index=0):
    for i in range(len(customization_list)):

        if customization_list[i].get_timestamp() == timestamp:
            command = customization_list[i].get_command()

            return command
    return False


def fetch_customization(index, timestamp):
    for i in range(len(customization_list)):

        if customization_list[i].get_timestamp() == timestamp:
            custom = customization_list[i]
            return custom

    return False


def alter_bit_order(custom, bit_to_be_changed, index):
    # print("button altered at ", index)
    command_string = custom.get_command()
    # print("**", command_string)
    chunk_size = 8
    bit_chunks = [command_string[i:i + chunk_size] for i in range(0, len(command_string), chunk_size)]
    # print("index", index)
    original_bits = list(bit_chunks[index])
    if original_bits[bit_to_be_changed] == "1":
        original_bits[bit_to_be_changed] = "0"
    elif original_bits[bit_to_be_changed] == "0":
        original_bits[bit_to_be_changed] = "1"
    new_bits = "".join(original_bits)
    bit_chunks[index] = new_bits
    new_command = "".join(bit_chunks)
    # print("new commadn ", new_command)
    custom.set_command(new_command)
    add_custom_to_list(custom, index)
    customize(paused, Flag, new_command)


def light_helper(command, row, column):
    indexes_to_light_up = []
    # print("commmand that entered light helper = ",command)
    location_of_button = [row, column]
    res = []
    for i in range(8):

        if command[i] == '1':
            indexes_to_light_up.append(i)
    res = [indexes_to_light_up, location_of_button]
    return res


def add_custom_to_list(custom, character_number):
    # print("character #" + str(character_number) + " is saved")
    custom.set_character_num(character_number + 1)

    if len(customization_list) == 0:
        customization_list.append(custom)
        stored_timestamps.append(custom.get_timestamp())
        return
    else:
        for customization in customization_list:
            if customization.get_timestamp() == custom.get_timestamp():
                customization_command_string = customization.get_command()
                custom_command_string = custom.get_command()
                chunk_size = 8
                bit_chunks_customization = [customization_command_string[i:i + chunk_size] for i in
                                            range(0, len(customization_command_string), chunk_size)]
                # print("customization in list ", bit_chunks_customization)
                bit_chunks_custom = [custom_command_string[i:i + chunk_size] for i in
                                     range(0, len(custom_command_string), chunk_size)]
                # print("custom in list ", bit_chunks_custom)
                new_bits = bit_chunks_custom[character_number]
                bit_chunks_customization[character_number] = new_bits
                new_command = "".join(bit_chunks_customization)
                customization.set_command(new_command)
                # print(customization.print_data())
                return

        customization_list.append(custom)
        stored_timestamps.append(custom.get_timestamp())
        print("stored timestamps ", stored_timestamps)
    if len(customization_list)!=0:
        for customs in customization_list:
            print("00000000  ",customs.print_data())



def customize(is_paused, helperFlag, new_command="0000000000000000000000000000000000000000000000000000000000000000"):
    # flag checks if song is playing
    exists_predecessor = False
    most_recent_command = "000"
    if len(customization_list) != 0:
        most_recent_customization = customization_list[-1]
        most_recent_command = most_recent_customization.get_command()
        exists_predecessor = True

    global Flag
    Flag = helperFlag
    if Flag:

        global paused
        paused = is_paused

        if not paused:
            pause(paused)

        current_time = pygame.mixer.music.get_pos() / 1000

        minutes, seconds = divmod(current_time, 60)
        seconds, milliseconds = divmod(seconds, 1)
        frame_grid = Frame(root)
        frame_grid.place(x=100, y=80)
        frames = []
        command_list = []
        for i in range(8):
            frame = Frame(frame_grid)
            frame.grid(row=i // 4, column=i % 4, padx=20, pady=10)

            frames.append(frame)

        # Create buttons in each frame labeled from 1 to 8
        previous_flag = False
        for i in range(8):
            button_counter = 1
            helpVar = 0
            counter2 = 1
            character_counter = 1
            exists = fetch_customization(i, current_time)
            button_list = []
            if len(customization_list) != 0:
                previous_flag = True

            for row in range(4):
                for col in range(2):

                    if exists:
                        custom = exists

                        custom.set_command(exists.get_command())

                        # save_button = Button(frames[i], text="save", command=lambda i=i: add_custom_to_list(custom, i))
                        # save_button.grid(row=2, column=3, padx=10)

                        button = Button(frames[i], text="LED# " + str(button_counter) + "@" + str(i + 1),
                                        command=lambda helpVar=helpVar, i=i: [alter_bit_order(custom, helpVar, i)])

                        customization = fetch_customization(i, current_time)
                        customization_command_string = customization.get_command()
                        chunk_size = 8
                        bit_chunks_customization = [customization_command_string[i:i + chunk_size] for i in
                                                    range(0, len(customization_command_string), chunk_size)]
                        current_command = bit_chunks_customization[i]

                        res = light_helper(current_command, row, col)

                        index_to_light = res[0]

                        if "1" in current_command:
                            for index in range(len(index_to_light)):
                                if index_to_light[index] == button_counter - 1:
                                    button.config(bg="yellow")

                        button.grid(row=row, column=col, padx=5, pady=5)

                        helpVar += 1
                        button_counter += 1

                    elif not exists and not exists_predecessor:
                        print("entered")

                        custom = Customization(character_counter, round(my_slider.get()*2)/2,
                                               new_command)

                        character_counter += 1

                        button = Button(frames[i], text="LED# " + str(button_counter) + "@" + str(i + 1),
                                        command=lambda helpVar=helpVar, i=i: [alter_bit_order(custom, helpVar, i)])
                        button.grid(row=row, column=col, padx=5, pady=5)
                        # save_button = Button(frames[i], text="save", command=lambda i=i: add_custom_to_list(custom, i))
                        # save_button.grid(row=2, column=3, padx=10)
                        helpVar += 1
                        button_counter += 1
                    elif not exists and exists_predecessor:

                        custom = Customization(character_counter, round(my_slider.get()*2)/2,
                                               most_recent_command)
                        character_counter += 1

                        button = Button(frames[i], text="LED# " + str(button_counter) + "@" + str(i + 1),
                                        command=lambda helpVar=helpVar, i=i: [alter_bit_order(custom, helpVar, i)])

                        chunk_size = 8
                        bit_chunks_customization = [most_recent_command[i:i + chunk_size] for i in
                                                    range(0, len(most_recent_command), chunk_size)]
                        current_command = bit_chunks_customization[i]

                        res = light_helper(current_command, row, col)
                        index_to_light = res[0]

                        if "1" in current_command:
                            for index in range(len(index_to_light)):
                                if index_to_light[index] == button_counter - 1:
                                    button.config(bg="yellow")

                        button.grid(row=row, column=col, padx=5, pady=5)
                        # save_button = Button(frames[i], text="save", command=lambda i=i: add_custom_to_list(custom, i))
                        # save_button.grid(row=2, column=3, padx=10)
                        helpVar += 1
                        button_counter += 1


my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360, state='disabled')
my_slider.place(x=345, y=430)

slider_label = Label(root, text="0")
slider_label.pack(pady=10)
root.mainloop()
