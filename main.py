import os
import asyncio
import signal
import discord
from discord.ext import commands

TOKEN    = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL  = int(os.getenv("CHANNEL"))
PREFIX   = "!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, self_bot=True, intents=intents)

@bot.event
async def on_ready():
    bot.loop.create_task(stay_in_vc())

async def stay_in_vc():
    await bot.wait_until_ready()
    guild   = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL)
    while True:
        try:
            if not guild.voice_client or not guild.voice_client.is_connected():
                await channel.connect()
                print("Reconectado ao canal de voz.")
        except Exception as e:
            pass  # silencioso
        await asyncio.sleep(2)

# ---------- ignora SIGTERM/SIGINT ----------
import signal
for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, signal.SIG_IGN)

# ---------- start (único "run") ----------
bot.run(TOKEN)
