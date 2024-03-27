import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online" 

GUILD_ID = "1168551939299086386" 
CHANNEL_ID = "1170013140193390632"
SELF_MUTE = False
SELF_DEAF = False

token = os.environ.get("TOKEN")
if not token:
  print("[ERROR] Please add a token inside Secrets.")
  sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
  print("[ERROR] Your token might be invalid. Please check it again.")
  sys.exit()

userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    
    auth = {"op": 2,"d": {"token": token,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
    
    vc = {"op": 4,"d": {"guild_id": GUILD_ID,"channel_id": CHANNEL_ID,"self_mute": SELF_MUTE,"self_deaf": SELF_DEAF}}
    ws.send(json.dumps(vc)) 
    
    ws.send(json.dumps(auth))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1,"d": None}))

def run_joiner():
  os.system("clear")
  print("Logged in as {}#{} ({}).".format(username, discriminator, userid))
  while True:
    joiner(token, status)
    time.sleep(30)

keep_alive()
run_joiner()