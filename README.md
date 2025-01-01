# LED Pattern Generator and Music Player 🎵💡

This project is a **custom LED pattern generator and music player interface** built with **Python**. It combines music playback functionality with LED visualization synchronized to specific timestamps in the song. The interface allows users to customize LED patterns, manage routines, and save them for future use.

---

## Features 🚀

### 🎶 Music Player
- Play, pause, and restart songs using an intuitive GUI built with **Tkinter**.
- Slider-based navigation through the song timeline.
- Integrated with **Pygame** for `.mp3` music playback.

### 💡 LED Visualization
- Displays LED patterns corresponding to specific timestamps in the song.
- Real-time dynamic visualization with customizable patterns.
- Uses a button grid to represent LEDs, where users can toggle states (on/off).

### 📂 CSV Integration
- Import routines (LED patterns and timestamps) from CSV files.
- Export new or edited routines to CSV for reuse.
- Handles multiple routines through file selection.

### 🛠 Customization
- Easily modify LED patterns using the GUI.
- Create new routines or edit existing ones by interacting with the LED visualization.

---

## Requirements 📋

Make sure you have the following installed:
- Required Python libraries:
  - `pygame`
  - `mutagen`
  - `tkinter`

You can install the required dependencies using:

```bash
pip install pygame mutagen tkinter

```

## Usage 🖥️

### Adding Songs
1. Go to the menu bar and click on **"Add songs!!"**.
2. A file dialog will open. Select a `.mp3` file from your system.
3. The selected song will be added to the playlist in the interface.

### Importing Routines
1. Go to the menu bar and click on **"Select routine"**.
2. A file dialog will open. Select a CSV file containing LED patterns and timestamps.
3. The imported routine will be loaded into the application.

### Playing Music
1. Click on a song in the playlist to highlight it.
2. Press the **"Play"** button to start playback.
3. Use the **Pause** button to pause and resume playback.
4. Press the **Restart** button to restart the song from the beginning.

### Customizing LED Patterns
1. Use the slider at the bottom of the interface to navigate to a specific timestamp in the song.
2. Click on the **"Customize!"** button to enter customization mode.
3. In the LED grid, click on individual LEDs to toggle their state (on/off).
4. After making changes, click **Finish** to save the customized routine.



 
