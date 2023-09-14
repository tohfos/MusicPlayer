class CustomizationWidget(Frame):
    def __init__(self, master, command):
        super().__init__(master)
        self.command = command

        # Create 8 frames to hold the buttons
        self.frames = []
        for i in range(8):
            frame = Frame(self,bg="red")
            self.frames.append(frame)
            frame.grid(row=i, column=i, padx=5, pady=5, sticky='nsew')

        # Create 64 buttons, placing them within the frames
        self.buttons = []
        for i in range(64):
            frame_index = i // 8  # Determine the frame index for this button
            button = Button(self.frames[frame_index], text=str(i), command=lambda i=i: self.toggle_value(i))
            self.buttons.append(button)
            button.grid(row=i % 8, column=0, padx=2, pady=2, sticky='nsew')

        self.update_buttons()


        #self.update_buttons()

    def toggle_value(self, index):
        # Toggle the value (0 to 1 or 1 to 0)
        current_value = self.command[index]
        new_value = '1' if current_value == '0' else '0'
        self.command = self.command[:index] + new_value + self.command[index + 1:]
        self.update_buttons()

    def update_buttons(self):
        # Update button labels based on the command string
        for i, button in enumerate(self.buttons):
            button.config(text=self.command[i])
            if self.command[i] == '1':
                button.config(bg='yellow')