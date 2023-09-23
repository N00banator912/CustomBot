# *********************************************************************
# Widget Base Class
# A basic widget for new widgets to inherit from
# *********************************************************************
# Author: K. E. Brown
# Started: 9/21/2023
# Modified: 9/23/2023
# *********************************************************************

class Widget:
    def __init__(self, ws, scene_name):
        self.ws = ws
        self.name = "Widget"
        self.desc = "A widget"
        self.nameAbbrv = "WDG"
        self.is_running = False
        self.commands = [self.help_command]

    def init(self):
        # Initialize widget resources here
        pass

    def start(self):
        # Start any background processes or actions here
        pass

    def update(self):
        # Implement widget logic here
        pass

    def pause(self):
        # Pause or stop any ongoing actions here
        pass

    def stop(self):
        # Clean up and stop the widget here
        pass

    def handle_interruption(self):
        # Handle interruptions or errors gracefully here
        pass

    def interrupt(self):
        self.is_running = False
        
    def help_command(self, args):
         # Generate a list of available commands for the widget
        available_commands = [cmd.__name__ for cmd in self.commands]

        # Create a help message with the list of commands
        help_message = f"Available commands for {self.name} ({self.desc}):\n"
        for cmd_name in available_commands:
            help_message += f"!{cmd_name}\n"

        # Send the help message to the chat
        self.send_message(help_message)