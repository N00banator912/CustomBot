# ******************************************************************************************************
# Muse Widget
# A simple widget for playing music from a youtube playlist
# ******************************************************************************************************
# Author: K. E. Brown
# Started: 9/27/2023
# Modified: 9/27/2023
# ******************************************************************************************************

import random
import os
import time

from Widget import Widget
from Commands.Command import Command

class MuseWidget(Widget):
    def __init__(self, ws, scene_name):
        self.is_playing = False
        self.on_shuffle = False
        self.play_on_start = True
        self.playlist = None
        self.current_song = None
        self.on_deck
    
    # Text displaying the current and next songs
    def playing_text(self):
        text = "Playing: "
        if self.is_playing:
            text += self.current_song.to_text()
        if self.on_deck != None:
            text += " | Next: " + self.on_deck.to_text()
        
        return text

    # Start the widget
    def start(self):
        super().start()
        self.is_running = True
        
        if self.play_on_start:
            self.play()
        
    # Play the next song
    def play(self):
        self.is_playing = True
        

class Song():
    def __init__(self, song_name, song_url):
        self.name = song_name
        self.suggested_by = None

        # Get the full name of the song from the youtube url
        self.fullname = None
        self.url = song_url
   
    # The song in text form
    def to_text(self):
        text = ""
        text += self.name
        if self.suggested_by != None:
            text += " (Suggested by " + self.suggested_by + ")"
        
        return text

