class Customization:
    _timestamp = 0
    command = "0000000000000000000000000000000000000000000000000000000000000000"
    character_num = 0



    def __init__(self,character_num, _timestamp,command):
        self._timestamp = _timestamp
        self.command = command
        self.character_num=character_num


    def print_data(self):
        list = [ self.command, self._timestamp,self.character_num]
        return list

    def get_timestamp(self):
        return self._timestamp



    def get_command(self):
        return self.command

    def set_command(self,new_command):
        self.command = new_command
    def get_character_num(self):
        return self.character_num
    def set_character_num(self,character_num):
        self.character_num=character_num
