import time
from tkinter import *
# from PIL import Image, ImageTk
from queue import Queue
from mutagen.mp3 import MP3
import pygame
import csv
import os
from tkinter import filedialog
from customization import Customization

customization_list = []

root = Tk()
root.title('LED-Pattern')
root.iconbitmap("images/Icon2.ico")
root.geometry("1000x500")
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
ControlFrame.place(x=310, y=420)
playButton = Button(ControlFrame, text="Play", font=("Helvetica", 16), command=lambda: helper(Flag))
statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
customizeButton = Button(ControlFrame, text="Customize!", command=lambda: customize(paused, Flag),
                         font=("Helvetica", 16))
finish_button = Button(ControlFrame, text="Finish", font=("Helvetica", 16),
                       command=lambda: [create_and_saveCsv(csvCounter), root.destroy()])

# playButton.place(x=300,y=450)
playButton.grid(row=0, column=0)
finish_button.grid(row=0, column=5)

pauseButton = Button(ControlFrame, text="Pause", command=lambda: pause(paused), font=("Helvetica", 16))
pauseButton.grid(row=0, column=1)
restartButton = Button(ControlFrame, text="Restart", command=lambda: Restart(paused, Flag), font=("Helvetica", 16))
restartButton.grid(row=0, column=2)

customizeButton.grid(row=0, column=3)

# pauseButton.place(x=360,y=450)


statusBar.pack(fill=X, side=BOTTOM, ipady=2)


def play_time():
    # Get Elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    current_time += 0.05  # Add 50 milliseconds (0.05 seconds)

    minutes, seconds = divmod(current_time, 60)
    seconds, milliseconds = divmod(seconds, 1)

    # Convert to formatted string
    converted_currentTime = f'{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 1000):03}'

    # Get the currently selected song
    song = song_box.get(ACTIVE)
    song_path = f'C:/Users/ahmed/MusicPlayer-remade/Songs/{song}.mp3'
    song_mut = MP3(song_path)
    song_length = song_mut.info.length

    # Convert the song length to formatted string
    minutes, seconds = divmod(song_length, 60)
    seconds, milliseconds = divmod(seconds, 1)
    converted_SongLen = f'{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 1000):03}'

    # Update the status bar with elapsed time and song length
    if converted_currentTime == converted_SongLen:
        statusBar.config(text=f'Time Elapsed: {converted_currentTime} of {converted_SongLen}')
        return converted_currentTime
    else:
        statusBar.config(text=f'Time Elapsed: {converted_currentTime} of {converted_SongLen}')

    # Schedule the function to run again after 50 ms (50 milliseconds)
    statusBar.after(50, play_time)
    return converted_currentTime


def play(PlayFlag):
    global csvCounter
    csvCounters = csvCounter
    global Flag
    Flag = PlayFlag
    song = song_box.get(ACTIVE)
    if csvCounters == 0:
        read_csv_and_add_to_list(song)
        csvCounter += 1

    song = f'C:/Users/ahmed/MusicPlayer-remade/Songs/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    Flag = True
    play_time()
    playButton.config(bg='cyan')


def pause(is_paused):
    # TODO obtain timestamps when paused

    if Flag:
        global paused
        paused = is_paused
        if paused:
            pauseButton.config(text="pause")
            pygame.mixer.music.unpause()
            paused = False
        elif not paused:
            pauseButton.config(text="resume")
            pygame.mixer.music.pause()
            paused = True


def Restart(is_paused, helperFlag):
    global paused
    paused = is_paused
    pygame.mixer.music.stop()
    if paused:
        pauseButton.config(text="pause")
        paused = False

    global Flag
    Flag = helperFlag
    play(Flag)


def fetch_command_for_character(index, timestamp):

    for i in range(len(customization_list)):

        if customization_list[i].get_timestamp() == timestamp :
            command = customization_list[i].get_command()
            chunk_size = 8
            bit_chunks = [command[i:i + chunk_size] for i in range(0, len(command), chunk_size)]

            return bit_chunks[index]
    return False


def fetch_command(index, timestamp):
    for i in range(len(customization_list)):

        if customization_list[i].get_timestamp() == timestamp and customization_list[i].get_character_num() == index:
            command = customization_list[i].get_command()

            return command
    return False
def fetch_customization(index, timestamp):

    for i in range(len(customization_list)):

        if customization_list[i].get_timestamp() == timestamp :
            custom = customization_list[i]
            return custom

    return False


def alter_bit_order(custom, bit_to_be_changed, index):
    print("button altered at ",index)
    command_string = custom.get_command()
    print("**",command_string)
    chunk_size = 8
    bit_chunks = [command_string[i:i + chunk_size] for i in range(0, len(command_string), chunk_size)]
    print("index", index)
    original_bits = list(bit_chunks[index])
    if original_bits[bit_to_be_changed] == "1":
        original_bits[bit_to_be_changed] = "0"
    elif original_bits[bit_to_be_changed] == "0":
        original_bits[bit_to_be_changed] = "1"
    new_bits = "".join(original_bits)
    bit_chunks[index] = new_bits
    new_command = "".join(bit_chunks)
    print("new commadn ",new_command)
    custom.set_command(new_command)

def light_helper(command,row,column):
    indexes_to_light_up = []
    location_of_button = [row,column]
    res = []
    for i in range(8):
        if command[i] == '1':
            indexes_to_light_up.append(i)
    res = [indexes_to_light_up,location_of_button]
    return res



def add_custom_to_list(custom,character_number):
    print("character #" + str(character_number)+" is saved")
    custom.set_character_num(character_number+1)

    if len(customization_list) == 0:
        customization_list.append(custom)
        return
    else:
        for customization in customization_list:
            if customization.get_timestamp() == custom.get_timestamp():
                customization_command_string = customization.get_command()
                custom_command_string = custom.get_command()
                chunk_size = 8
                bit_chunks_customization = [customization_command_string[i:i + chunk_size] for i in range(0, len(customization_command_string), chunk_size)]
                print("customization in list ",bit_chunks_customization)
                bit_chunks_custom = [custom_command_string[i:i + chunk_size] for i in range(0, len(custom_command_string), chunk_size)]
                print("custom in list ", bit_chunks_custom)
                new_bits = bit_chunks_custom[character_number]
                bit_chunks_customization[character_number] = new_bits
                new_command= "".join(bit_chunks_customization)
                customization.set_command(new_command)
                print(customization.print_data())
                return

        customization_list.append(custom)
    for customizable in range(len(customization_list)):
        print("customizable " ,customization_list[customizable].print_data())
    print("customization list has" + str(len(customization_list)) +" elements")

def customize(is_paused, helperFlag):
    # flag checks if song is playing

    global Flag
    Flag = helperFlag
    if Flag:

        global paused
        paused = is_paused

        if not paused:
            pause(paused)
        current_time = pygame.mixer.music.get_pos() / 1000
        current_time += 0.05  # Add 50 milliseconds (0.05 seconds)

        minutes, seconds = divmod(current_time, 60)
        seconds, milliseconds = divmod(seconds, 1)
        frame_grid = Frame(root)
        frame_grid.place(x=0, y=80)
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

            if len(customization_list) != 0:
                previous_flag = True


            for row in range(4):
                for col in range(2):

                    if exists:
                        custom = exists



                        custom.set_command(exists.get_command())

                        save_button = Button(frames[i], text="save", command=lambda i=i: add_custom_to_list(custom, i))
                        save_button.grid(row=2, column=3, padx=10)

                        button = Button(frames[i], text="LED# " + str(button_counter) + "@" + str(i + 1),command=lambda helpVar=helpVar, i=i: [alter_bit_order(custom, helpVar, i)])

                        customization = fetch_customization(i,current_time)
                        customization_command_string = customization.get_command()
                        chunk_size = 8
                        bit_chunks_customization = [customization_command_string[i:i + chunk_size] for i in range(0, len(customization_command_string), chunk_size)]
                        current_command = bit_chunks_customization[i]

                        res = light_helper(current_command,row,col)
                        index_to_light =res[0]
                        
                        if "1" in current_command:
                            for index in range(len(index_to_light)):
                                if index_to_light[index] == button_counter-1:
                                    button.config(bg="yellow")



                        button.grid(row=row, column=col, padx=5, pady=5)
                        helpVar += 1
                        button_counter += 1








                    if not exists:
                        custom = Customization(character_counter,current_time,"0000000000000000000000000000000000000000000000000000000000000000")
                        character_counter+=1

                        button = Button(frames[i], text="LED# " + str(button_counter) + "@" + str(i + 1),command=lambda helpVar=helpVar, i=i: [alter_bit_order(custom, helpVar, i)])
                        button.grid(row = row,column=col,padx=5,pady=5)
                        save_button = Button(frames[i], text="save", command=lambda i=i: add_custom_to_list(custom, i))
                        save_button.grid(row=2, column=3, padx=10)
                        helpVar += 1
                        button_counter += 1











        # confirm_button = Button(root, text="confirm ")
        # confirm_button.place(x=800,y=200)

        # Convert to formatted string
        # converted_currentTime = f'{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 1000):03}'


root.mainloop()