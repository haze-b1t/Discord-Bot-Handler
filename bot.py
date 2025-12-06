# -*- Dependencies Installer -*-

import subprocess
import sys
import os
import importlib

def install_requirements(requirements_file="requirements.txt"):
    if not os.path.exists(requirements_file):
        print(f"[!] {requirements_file} not found.")
        return

    with open(requirements_file, "r") as file:
        requirements = [r.strip() for r in file.readlines() if r.strip()]

    missing = []

    for req in requirements:
        # Extract importable module name (best guess)
        # e.g. "discord.py" → "discord"
        pkg = req.split("==")[0].replace("-", "_").split(".")[0]

        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(req)

    if missing:
        print(f"[+] Installing missing packages: {missing}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    else:
        print("[+] All dependencies already installed.")

install_requirements()

# -=- Bot Client -=- #

import asyncio
import discord
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

clientName = "your_name"
version = "25w49b"
authors = "haze (@haze_b1t)"

bot_running = False
bot_loop = None

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

# =-------------------------------------------------------------------------------------------------------------------------------------=

root.overrideredirect(True)

title_bar = tk.Frame(root, bg="#0F0F0F", height=26)
title_bar.pack(fill="x")

title_label = tk.Label(
    title_bar,
    text="_b1t CLI",
    fg="#00FF00",
    bg="#0F0F0F",
    font=("Courier New", 10, "bold")
)
title_label.pack(side="top", pady=2)

button_container = tk.Frame(title_bar, bg="#0F0F0F")
button_container.place(relx=1.0, rely=0.5, anchor="e")

# XP-style button colors
BTN_BG = "#C0C0C0"
BTN_BORDER = "#404040"
BTN_HOVER = "#D6D6D6"
BTN_ACTIVE = "#A0A0A0"
BTN_FG = "black"

def xp_button(widget):
    widget.configure(
        relief="flat",
        bg=BTN_BG,
        fg=BTN_FG,
        activebackground=BTN_ACTIVE,
        width=3,
        height=1,
        highlightthickness=1,
        highlightbackground=BTN_BORDER,
        highlightcolor=BTN_BORDER,
        font=("Tahoma", 9)
    )
    def on_enter(e):
        widget.config(bg=BTN_HOVER)
    def on_leave(e):
        widget.config(bg=BTN_BG)
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# -=- Minimize -=- #
def minimize():
    root.update_idletasks()
    root.overrideredirect(False)
    root.iconify()
    root.after(10, lambda: root.overrideredirect(True))

# -=- Maximize (REAL monitor-aware) -=- #
def maximize():
    root.update_idletasks()

    if not getattr(root, "_max", False):
        root._max = True
        root._restore_geom = root.geometry()

        x = root.winfo_rootx()
        y = root.winfo_rooty()

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()

        # Get the monitor bounds for the CURRENT monitor
        monitor = root.winfo_screen()
        screen_x = root.winfo_vrootx()
        screen_y = root.winfo_vrooty()

        root.geometry(f"{screen_w}x{screen_h}+{screen_x}+{screen_y}")
    else:
        root.geometry(root._restore_geom)
        root._max = False

# -=- Close -=- #
def close_window():
    try:
        stop_bot()
    except:
        pass
    root.destroy()

minimize_btn = tk.Button(button_container, text="_", command=minimize)
maximize_btn = tk.Button(button_container, text="□", command=maximize)
close_btn = tk.Button(button_container, text="X", command=close_window)

xp_button(minimize_btn)
xp_button(maximize_btn)
xp_button(close_btn)

minimize_btn.pack(side="left", padx=(0,2))
maximize_btn.pack(side="left", padx=(0,2))
close_btn.pack(side="left")

# -=- Drag window -=- #
def start_move(event):
    root._offsetx = event.x
    root._offsety = event.y

def do_move(event):
    x = event.x_root - root._offsetx
    y = event.y_root - root._offsety
    root.geometry(f"+{x}+{y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)

# -=- Resize Grip -=- #
resize_grip = tk.Frame(root, cursor="size_nw_se", bg="#303030")
resize_grip.place(relx=1.0, rely=1.0, anchor="se", width=16, height=16)

def do_resize(event):
    new_w = event.x_root - root.winfo_rootx()
    new_h = event.y_root - root.winfo_rooty()
    if new_w > 250 and new_h > 200:
        root.geometry(f"{new_w}x{new_h}")

resize_grip.bind("<B1-Motion>", do_resize)

# =-------------------------------------------------------------------------------------------------------------------------------------=


minimize_btn.pack(side="left", padx=2)
maximize_btn.pack(side="left")

title_label.pack(side="left", padx=8)

terminal = scrolledtext.ScrolledText(
    root, width=70, height=20,
    bg="#202020", fg="#00FF00",
    font=("Courier New", 10),
    bd=2, relief="sunken",
    wrap="word"
)
terminal.pack(padx=10, pady=10, fill="both", expand=True)

class TerminalRedirect:
    def write(self, text):
        terminal.insert(tk.END, text)
        terminal.see(tk.END)

    def flush(self):
        pass

import sys
sys.stdout = TerminalRedirect()

entry_frame = tk.Frame(root, bg="#202020")
entry_frame.pack(fill="x", padx=10, pady=(0, 10))

entry_frame.columnconfigure(0, weight=0)
entry_frame.columnconfigure(1, weight=1)

cmd_label = tk.Label(entry_frame, text="Command:", bg="#202020", fg="#00FF00", font=("Courier New", 8))
cmd_label.grid(row=0, column=0)

cmd_entry = tk.Entry(entry_frame, width=50, bg="#202020", fg="#00FF00", font=("Courier New", 8))
cmd_entry.grid(row=0, column=1, padx=5, sticky="ew")

# -=- Command Handler -=- # 
def handle_command(event=None):
    command = cmd_entry.get().strip()
    cmd_entry.delete(0, tk.END)

    if command == "start":
        start_bot()
    elif command == "stop":
        stop_bot()
    elif command == "quit":
        stop_bot()
        root.destroy()
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Unknown command: {command}")

cmd_entry.bind("<Return>", handle_command)

# -=- Client UI Start -=- # 
print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> CLI Ready. Use \"start\" to start the bot, \"stop\" to stop the bot, or \"quit\" to close the CLI.")
root.mainloop()
