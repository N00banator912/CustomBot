# ******************************************************************************************************
# Puns Widget
# A Widget that sends a random pun to chat
# This is a great example of a widget which uses File I/O
# ******************************************************************************************************
# Author: K. E. Brown
# Started: 9/23/2023
# Modified: 9/23/2023
# ******************************************************************************************************

import random
import os

from Widget import Widget
from Command import Command

class PunsWidget(Widget):
    def __init__(self, ws, scene_name):
        super().__init__(ws, scene_name)
        self.name = "Puns"
        self.desc = "A widget for puns"
        self.nameAbbrv = "PUN"

    def start(self):
        super().start()
        self.is_running = True

    def update(self):
        super().update()

        # Implement widget logic here
        if self.is_running:
            self.send_random_pun()

    def send_random_pun(self):
        puns_file = "Data/Puns.txt"
        if os.path.exists(puns_file):
            with open(puns_file, "r") as file:
                puns = file.readlines()
                if puns:
                    random_pun = random.choice(puns).strip()
                    self.send_message(random_pun)

class PunsCommand(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "Pun"
        self.desc = "Get a random pun"

    def execute(self, username, args):
        # Execute command logic here
        puns_widget = self.bot.get_widget_by_name("Puns")  # Assuming you have a method to get the widget by name
        puns_widget.send_random_pun()
