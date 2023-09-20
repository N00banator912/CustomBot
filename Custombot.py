import cv2
import importlib.util
import json
import os
import requests
import websocket
import asyncio
import websockets

from irc.bot import SingleServerIRCBot

class CustomBot(SingleServerIRCBot):
    def __init__(self):
        self.bot_username = None
        self.channel_username = None
        self.oauth_token = None
        self.client_id = None
        self.user_obs_port = 59650
        self.user_obs_ips = []
        self.ws_server = None  # WebSocket server

        # Initialize the IRC bot
        super().__init__([], "", "")  # We'll set these values later

        # Load data and components
        self.load_data_and_components("Kat.data")

    async def start_websocket_server(self):
        # Define WebSocket server logic
        async def server(websocket, path):
            async for message in websocket:
                # Handle incoming WebSocket messages
                print(f"Received WebSocket message: {message}")
                # Add your custom WebSocket logic here

        # Start the WebSocket server
        self.ws_server = await websockets.serve(server, "localhost", 8765)

        # Initialize the IRC bot
        super().__init__([], "", "")  # We'll set these values later
          
        # Start the WebSocket server
        self.start_websocket_server()
        
        # Load data and components
        self.load_data_and_components("Kat.data")

    def load_data_and_components(self, filename):
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        if len(lines) >= 4:
            self.bot_username = lines[0]
            self.channel_username = lines[1]
            self.oauth_token = self.generate_oauth_token(lines[2], lines[3])
            self.client_id = lines[3]
            self.user_obs_ips = lines[4].split(',')
        else:
            print("Error: Kat.data file does not contain sufficient data.")

        # Initialize the IRC bot with the OAuth token and channel
        super().__init__([(self.channel_username, self.oauth_token)], self.bot_username, self.bot_username)

        self.load_widgets()
        self.load_commands()

    def generate_oauth_token(self, client_id, client_secret):
        token_url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
        response = requests.post(token_url)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("access_token")
        else:
            print("Error generating OAuth token")
            return None

    def load_widgets(self):
        widget_folder = "Widgets"
        widget_files = [f for f in os.listdir(widget_folder) if f.endswith(".py")]

        for widget_file in widget_files:
            module_name = os.path.splitext(widget_file)[0]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(widget_folder, widget_file))
            widget_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(widget_module)

            widget_instance = getattr(widget_module, module_name)()
            self.widgets.append(widget_instance)

            if hasattr(widget_module, "commands"):
                self.commands.extend(widget_module.commands)

    def load_commands(self):
        command_folder = "Commands"
        command_files = [f for f in os.listdir(command_folder) if f.endswith(".py")]

        for command_file in command_files:
            module_name = os.path.splitext(command_file)[0]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(command_folder, command_file))
            command_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(command_module)

            # Create an instance of the command class and append it to the commands list
            command_instance = getattr(command_module, module_name)(self)
            self.commands.append(command_instance)

    def start_websocket_server(self):
        # Define WebSocket server logic
        async def server(websocket, path):
            async for message in websocket:
                # Handle incoming WebSocket messages
                print(f"Received WebSocket message: {message}")
                # Add your custom WebSocket logic here

        # Start the WebSocket server
        self.ws_server = websockets.serve(server, "localhost", self.user_obs_port)

        async def run_server():
            async with self.ws_server:
                await self.ws_server.serve_forever()

        asyncio.get_event_loop().run_until_complete(run_server())

    def connect_to_obs(self):
        for ip in self.user_obs_ips:
            try:
                obs_ws_url = f"ws://{ip}:{self.user_obs_port}/api"
                self.ws = websocket.create_connection(obs_ws_url)
                print("Connected to Streamlabs OBS WebSocket")
                break
            except Exception as e:
                print(f"Error connecting to {ip}: {e}")

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def on_pubmsg(self, connection, event):
        message = event.arguments[0]
        username = event.source.split('!')[0]

        # Check if the message is a command
        if message.startswith('!'):
            self.handle_command(username, message[1:])

    def handle_command(self, username, command):
        # Check if the command is within the list of loaded commands
        command_name = command.split(" ")[0].lower()
        for cmd in self.commands:
            if cmd.name_abbrv.lower() == command_name:
                cmd.execute(username, command)
                break

    def switch_scene(self, scene_name):
        # Implement logic to switch scenes here
        # For example:
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "SetCurrentScene",
            "params": {
                "scene-name": scene_name
            }
        }
        self.ws.send(json.dumps(message))

    def main(self):
        # Connect to Streamlabs OBS WebSocket
        self.connect_to_obs()
        if not self.ws:
            return

        # Initialize widgets
        for widget in self.widgets:
            widget.init()

        # Start widgets
        for widget in self.widgets:
            widget.start()

        # Start the IRC bot
        self.start()
        
        asyncio.get_event_loop().run_until_complete(self.start_websocket_server())

    def update(self):
        for widget in self.widgets:
            widget.update()

    def shutdown(self):
        # Release resources
        cv2.destroyAllWindows()
        self.ws.close()
        for widget in self.widgets:
            widget.stop()
            
        if self.ws_server:
            self.ws_server.close()
            asyncio.get_event_loop().run_until_complete(self.ws_server.wait_closed())            

        print("Disconnected from Streamlabs OBS WebSocket")

# Actual Execution
if __name__ == "__main__":
    bot = CustomBot()
    bot.main()