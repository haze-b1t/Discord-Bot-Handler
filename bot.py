## ========= SSL Certification ========= ##

import os
import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

## ========= Dependencies ========= ##



## ========= Imports ========= ##

import sys
import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import threading
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path   # <-- needed for Documents folder handling

## ========= Theme ========= ##

THEME = {
    "bg": "#e1e1e1",
    "text": "#1e1e1e",
    "log_bg": "#1e1e1e",
    "log_text": "#00ff95",
    "button_bg": "#e5e5e5",
    "button_fg": "#1e1e1e",
    "button_active": "#e1e1e1",
    "border": "#333333"
}

## ========= Bot Setup ========= ##

load_dotenv()
token = os.getenv('TOKEN')
name = "Delta#6491"
version = "25w48e"
authors = "haze_b1t"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix='.',
    intents=intents,
    help_command=None  # <-- disables default help
)
tree = bot.tree
bot_running = False
bot_thread = None

def get_documents_folder():
    """Return Documents folder on Windows, macOS, and Linux."""
    home = Path.home()
    docs = home / "Documents"
    return docs if docs.exists() else home

def save_logs_to_file():
    """Save all logs to a timestamped .txt file in Documents."""
    try:
        logs = log_box.get("1.0", tk.END).strip()
        if not logs:
            return None

        documents = get_documents_folder()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = documents / f"DeltaBot_Logs_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(logs)

        return filename

    except Exception as e:
        log(f"Failed to save logs: {e}\n")
        return None

def log(text: str):
    # Base directory
    base_dir = os.path.join(os.getcwd(), "Haze's Discord Bots")

    # Bot-specific subfolder
    bot_dir = os.path.join(base_dir, name)

    # Create folders if they don't exist
    os.makedirs(bot_dir, exist_ok=True)

    # Log file (one per day)
    log_file_path = os.path.join(bot_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

    # Append log entry
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(text)
    # Also display in UI
    log_box.insert(tk.END, text)
    log_box.see(tk.END)

# -*- Events -*- #
@bot.event
async def on_ready():
    log(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Starting {bot.user}. | "
        f"ID: {bot.user.id} | Version: {version} | Authors: {authors}\n"
    )
    await bot.change_presence(activity=discord.Game(name="Type .help for commands"))

## ========= COMMANDS ========= ##
    # -- (New-ish) Slash Commands -- #
@tree.command(name="help", description="Show help message with available commands.")
async def slash_help(interaction: discord.Interaction):
    help_text = (
        "Delta Bot Commands:\n"
        "/help - Show this help message\n"
        "/ping - Check bot responsiveness\n"
        "/clear - Clear all messages in the current channel\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Slash Help command used by {interaction.user}\n")

@tree.command(name="ping", description="Check bot responsiveness.")
async def slash_ping(interaction: discord.Interaction):
    start = datetime.now()
    await interaction.response.send_message("Pong!")
    end = datetime.now()
    elapsed = (end - start).total_seconds() * 1000  # convert to ms
    await interaction.edit_original_response(content=f"Pong! `{elapsed:.2f}ms`")
    log(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Slash Ping command used by {interaction.user}."
        f" Response time: {elapsed:.2f}ms\n"
    )   
@tree.command(name="clear", description="Clear messages in the current channel.")
@commands.has_permissions(manage_messages=True)
async def slash_clear(interaction: discord.Interaction, amount: int = None, age_limit: bool = True):
    channel = interaction.channel
    author = interaction.user  
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Slash Clear command used by {author} in #{channel}\n")
    await asyncio.sleep(1)
    status_msg = await interaction.response.send_message("🧹 Clearing messages...")
    deleted = 0
    now = datetime.utcnow()
    DISCORD_MAX_AGE_DAYS = 14
    async for msg in channel.history(limit=None):
        if amount is not None and deleted >= amount:
            break
        if age_limit:
            message_age_days = (now - msg.created_at.replace(tzinfo=None)).days
            if message_age_days >= DISCORD_MAX_AGE_DAYS:
                continue
        try:
            await msg.delete()
            deleted += 1
            await asyncio.sleep(0.15)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry = getattr(e, "retry_after", 1)
                log(f"Rate limited. Waiting {retry} seconds...\n")
                await asyncio.sleep(retry)
            else:
                log(f"Delete error: {e}\n")
    await interaction.edit_original_response(content=f"✅ Deleted **{deleted} messages**.")
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Slash Clear finished in #{channel}. Deleted {deleted} messages.\n")



    # -- Classic Commands -- #
@bot.command(name='help')
async def help_command(ctx):
    help_text = (
        "Delta Bot Commands:\n"
        ".help - Show this help message\n"
        ".ping - Check bot responsiveness\n"
        ".clear - Clear all messages in the current channel\n"
    )
    await ctx.send(help_text)
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Help command used by {ctx.author}\n")

@bot.command(name='ping')
async def ping(ctx):
    start = datetime.now()
    message = await ctx.send("Pong!")
    end = datetime.now()
    elapsed = (end - start).total_seconds() * 1000  # convert to ms
    await message.edit(content=f"Pong! `{elapsed:.2f}ms`")
    log(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}) >> Ping command used by {ctx.author}."
        f"Response time: {elapsed:.2f}ms\n"
    )

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None, age_limit: bool = True):
    channel = ctx.channel
    author = ctx.author

    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Clear command used by {author} in #{channel}\n")
    await asyncio.sleep(1)
    status_msg = await ctx.send("🧹 Clearing messages...")

    deleted = 0
    now = datetime.utcnow()
    DISCORD_MAX_AGE_DAYS = 14

    async for msg in channel.history(limit=None):
        if amount is not None and deleted >= amount:
            break

        if age_limit:
            message_age_days = (now - msg.created_at.replace(tzinfo=None)).days
            if message_age_days >= DISCORD_MAX_AGE_DAYS:
                continue

        try:
            await msg.delete()
            deleted += 1
            await asyncio.sleep(0.15)

        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry = getattr(e, "retry_after", 1)
                log(f"Rate limited. Waiting {retry} seconds...\n")
                await asyncio.sleep(retry)
            else:
                log(f"Delete error: {e}\n")

    await status_msg.edit(content=f"✅ Deleted **{deleted} messages**.")
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Clear finished in #{channel}. Deleted {deleted} messages.\n")


## ========= Start/Stop Variables ========= ##

def run_bot():
    try:
        bot.run(token)
    except Exception as e:
        log(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Bot crashed: {e}\n")

def start_bot():
    global bot_running, bot_thread

    if bot_running:
        log("Bot is already running.\n")
        return

    bot_running = True
    log("Starting bot...\n")

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

def stop_bot():
    global bot_running

    if not bot_running:
        log("Delta#6491 is not running.\n")
        return

    log("Stopping Delta#6491...\n")
    bot_running = False

    # Save logs BEFORE closing
    file_path = save_logs_to_file()
    if file_path:
        log(f"Saved log file to: {file_path}\n")

    try:
        asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
    except Exception as e:
        log(f"Error stopping Delta#6491: {e}\n")
    finally:
        log(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')} >> Delta#6491 has been stopped.\n"
        )


## ========= UI Setup ========= ##

root = tk.Tk()
root.title("Bot Controller")
root.geometry("800x600")
root.resizable(False, False)

root.configure(bg=THEME["bg"])

    # -*- Log Frame (adds border & spacing) -*- #
log_frame = tk.Frame(root, bg=THEME["border"], highlightthickness=0)
log_frame.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)

log_box = scrolledtext.ScrolledText(
    log_frame,
    wrap=tk.WORD,
    height=12,
    bg=THEME["log_bg"],
    fg=THEME["log_text"],
    insertbackground=THEME["text"],
    borderwidth=0,
    highlightthickness=0
)
log_box.pack(fill=tk.BOTH, expand=True)

    # -*- Buttons -*- #
button_frame = tk.Frame(root, bg=THEME["bg"])
button_frame.pack(pady=10)

def themed_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        width=15,
        command=command,
        bg=THEME["button_bg"],
        fg=THEME["button_fg"],
        activebackground=THEME["button_active"],
        activeforeground=THEME["button_fg"],
        relief="flat",
        highlightthickness=2,
        highlightbackground=THEME["border"]
    )

start_button = themed_button(button_frame, "Start Bot", start_bot)
start_button.grid(row=0, column=0, padx=15)

stop_button = themed_button(button_frame, "Stop Bot", stop_bot)
stop_button.grid(row=0, column=1, padx=15)

def exit_program():
    log("Exiting program...\n")
    try:
        if bot_running:
            asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
    except:
        pass
    root.destroy()

exit_button = themed_button(button_frame, "Exit", exit_program)
exit_button.grid(row=0, column=2, padx=15)

    # -*- UI Loop -*- #
root.mainloop()


# lowkey used ai for a lot of this code, but I organized it!