import asyncio
import discord
import os
import time
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import threading
import tkinter as tk
from tkinter import scrolledtext

# -=- Token Loading & Client Initialization -=- # 
load_dotenv()
token = os.getenv('token')

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

clientName = "your_name_here"
version = "25w49a"
authors = "haze (@haze_b1t)"

bot_running = False
bot_loop = None

clientName = "_b1t"
version = "25w49a"
authors = "haze (@haze_b1t)"

# -=- Start Event -=- # 
@client.event
async def on_ready():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Logged in as {clientName}. | Version: {version} | Author(s): {authors}")
    time.sleep(1)
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> {clientName} is now running.")

# -=- Client Commands -=- # 

# -=- Client UI and CLI Commands -=- # 

# -- Start Bot Varible -- # 
def start_bot():
    global bot_running, bot_loop

    if bot_running:
        print(">> Bot is already running.")
        return

    bot_running = True
    bot_loop = asyncio.new_event_loop()

    def run():
        try:
            bot_loop.run_until_complete(client.start(token))
        except Exception as e:
            print(f">> Bot stopped: {e}")

    threading.Thread(target=run, daemon=True).start()
    print(">> Bot starting...")

# -- Stop Bot Varible -- # 
def stop_bot():
    global bot_running, bot_loop

    if not bot_running:
        print(">> Bot is not running.")
        return

    bot_running = False

    async def shutdown():
        await client.close()

    bot_loop.call_soon_threadsafe(lambda: asyncio.ensure_future(shutdown()))
    print(">> Bot stopping...")

# -=- Windows XP style CLI -=- # 
root = tk.Tk()
root.title("_b1t CLI")

root.configure(bg="#202020")

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.columnconfigure(0, weight=1)

terminal = scrolledtext.ScrolledText(
    root, width=70, height=20,
    bg="#202020", fg="#00FF00",
    font=("Courier New", 10),
    bd=2, relief="sunken",
    wrap="word"
)
terminal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

class TerminalRedirect:
    def write(self, text):
        terminal.insert(tk.END, text)
        terminal.see(tk.END)

    def flush(self):
        pass

import sys
sys.stdout = TerminalRedirect()

entry_frame = tk.Frame(root, bg="#202020")
entry_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

entry_frame.columnconfigure(0, weight=0)
entry_frame.columnconfigure(1, weight=1)

cmd_label = tk.Label(entry_frame, text="Command:", bg="#202020", fg="#00FF00", font=("Courier New", 8))
cmd_label.grid(row=0, column=0)

cmd_entry = tk.Entry(entry_frame, width=50, font=("Courier New", 12))
cmd_entry.grid(row=0, column=1, padx=5, sticky="ew")

# -=- Command Handler -=- # 
def handle_command(event=None):
    command = cmd_entry.get().strip()
    cmd_entry.delete(0, tk.END)

    if command == "/start":
        start_bot()
    elif command == "/stop":
        stop_bot()
    elif command == "/quit":
        stop_bot()
        root.destroy()
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Unknown command: {command}")

cmd_entry.bind("<Return>", handle_command)

# -=- Client UI Start -=- # 
print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> CLI Ready. Use \"/start\" to start the bot, \"/stop\" to stop the bot, or \"/quit\" to close the CLI.")
root.mainloop()
