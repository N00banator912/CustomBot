#**********************************************************************************************************************
# Custom Bot Core
# A simple to use, open source Twitch bot that allows you to create your own custom bot commands and widgets.
#**********************************************************************************************************************
# Author:   K. E. Brown
# Started:  9/17/2023
# Modified: 9/21/2023
#**********************************************************************************************************************

# Imports
from re import S
import cv2
import os
import json
import asyncio
import websockets
import socket
import requests
import time
from irc.bot import SingleServerIRCBot
import importlib.util

# Core Class
class CustomBot(SingleServerIRCBot):
    # Initialize the bot
    def __init__(self):
        self.get_user()
        self.load_data()

        # Initialize the IRC bot
        super().__init__([(self.channel_username, self.oauth_token)], self.bot_username, self.bot_username)
        
        self.obs_port = 4444

        self.start_websocket_server()
        self.connect_to_obs()
        self.connect_to_twitch()
        self.load_widgets()
        self.load_commands()


    # Prompt the user for their CustomBot username
    def get_user(self):
        self.local_username = input("Enter your CustomBot username: ")
        

    # Save the user's data to a .data file
    def save_data(self):
        # Save user data to .data file
        data = {
            "bot_username": self.bot_username,
            "channel_username": self.channel_username,
            "irc_clients": self.irc_clients,
            "user_obs_ips": self.user_obs_ips
        }

        with open(self.local_username + ".data", "w") as f:
            json.dump(data, f)
            
    # Load the user's data
    def load_data(self):
        # if the user already has a .data file, load it
        if os.path.exists(self.local_username + ".data"):
            with open(self.local_username + ".data", "r") as f:
                data = json.load(f)
                self.bot_username = data.get("bot_username")
                self.channel_username = data.get("channel_username")
                
                self.irc_clients = data.get("irc_clients", [])
                
                self.user_obs_ips = data.get("user_obs_ips", [])
        
        # otherwise, prompt the user for their information
        else:
            self.prompt_user_for_data()
           
        self.oauth_token = self.generate_oauth()

    def prompt_user_for_data(self):
        # Implement logic to prompt the user for their information and save it to a .data file
        self.bot_username = input("Enter your bot username: ")
        self.channel_username = input("Enter your channel username: ")
        
        # Prompt the user for all IRC clients they want to connect to
        # These should be stored as a list of ID, Secret, and Redirect URIs with a string for the user's client identifier (i.e. its name; "Twitch", "TikTok", etc)
        self.irc_clients = []
        
        while input("Add an IRC client? (y/n): ").lower() != "n":
            client = {}
            client["name"] = input("Enter the client name: ")
            client["id"] = input("Enter the client ID: ")
            client["secret"] = input("Enter the client secret: ")
            client["oauth_url"] = input("Enter the OAuth URL: ")
            self.irc_clients.append(client)
        
        self.user_obs_ips = input("Enter your OBS IP addresses (separated by commas): ").split(",")
        
        self.save_data()

    # Start the WebSocket server which will handle incoming and outgoing messages
    async def start_websocket_server(self):
        async def server(websocket, path):
            try:
                # Handle incoming WebSocket messages
                async for message in websocket:
                    print(f"Received WebSocket message: {message}")
                    # Add your custom WebSocket logic here
            except websockets.exceptions.ConnectionClosedError:
                # Handle connection closed gracefully
                pass

        # Start the server
        server_address = ("localhost", 8765)  # Update with your desired host and port
        self.ws_server = await websockets.serve(server, *server_address)

        # Keep the server running
        await self.ws_server.wait_closed()

    # Connect our bot to OBS
    async def connect_to_obs(self):
        # Connect to OBS WebSocket server
        slobs_ws_url = "ws://localhost:" + self.obs_port
    
        async with websockets.connect(slobs_ws_url) as websocket:
            # Send and receive WebSocket messages to control Streamlabs OBS
            await websocket.send('{"request-type": "GetVersion"}')
            response = await websocket.recv()
            print(f"Streamlabs OBS Version: {response}")

    # Connect our bot to various IRC clients like Twitch chat
    async def connect_to_irc(self):
        # Loop through all IRC clients and prompt the user to connect to them
        for client in self.irc_clients:
            if input(f"Connect to {client['name']}? (y/n): ").lower() == "y":
                # Connect to the IRC client asynchronously
                irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                irc.connect((client["server"], client["port"]))

                # Generate an OAuth token for the IRC client
                oauth = self.generate_oauth(client["id"], client["secret"], client["oauth_url"])

                # Authenticate with the IRC server using client ID, client secret, and OAuth token
                irc.send(bytes(f"PASS {client[oauth]}\r\n", "UTF-8"))
                irc.send(bytes("NICK " + self.bot_username + "\r\n", "UTF-8"))
                
                # Join the channel
                irc.send(bytes("JOIN " + client["channel"] + "\r\n", "UTF-8"))

                # Keep the IRC connection running asynchronously (you can add your message handling logic here)
                while True:
                    data = irc.recv(2048).decode("UTF-8")
                    self.update(data)
                    await asyncio.sleep(0.1)  # Sleep for a short duration to avoid busy-waiting
    
    # Generate an OAuth token for the IRC client
    def generate_oauth(self, client_id, client_secret, oauth_url):
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        
        response = requests.post(oauth_url, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print("Failed to obtain OAuth token.")
            return None

    # Load all Widgets in Widgets folder
    def load_widgets(self):
        self.widgets = []
        
        for file in os.listdir("Widgets"):
            if file.endswith(".py"):
                widget = importlib.import_module("Widgets." + file[:-3])
                self.widgets.append(widget)
                
    # Load all Commands in Commands folder
    def load_commands(self):
        self.commands = []
        
        for file in os.listdir("Commands"):
            if file.endswith(".py"):
                command = importlib.import_module("Commands." + file[:-3])
                self.commands.append(command)
             
        for widget in self.widgets:
            self.commands.append(widget.commands)

    # Process incoming messages
    async def update(self, message):
        # Implement your asynchronous logic here
        print(f"Received message: {message}")
        
        # if the message is a command, execute it
        if message.startswith("!"):
            # Parse the message
            command = message.split(" ")[0]
            args = message.split(" ")[1:]
   
            # Execute the command
            self.execute_command(command, args)

    # Main bot execution, though I think most of it is already in __init__
    def main(self):
        # Implement the main bot loop
        pass

if __name__ == "__main__":
    bot = CustomBot()
    bot.main()