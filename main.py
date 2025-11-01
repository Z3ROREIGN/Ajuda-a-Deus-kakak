import os
import asyncio
import signal       # <-- agora está presente
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
    print(f"{bot.user} ONLINE")
    bot.loop.create_task(stay_in_vc())

async def stay_in_vc():
    await bot.wait_until_ready()
    guild   = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL)
    while True:
        try:
            if guild.voice_client is None or not guild.voice_client.is_connected():
                await channel.connect()
                print("Reconectado no canal de voz:", channel.name)
        except Exception as e:
            print("Erro ao reconectar:", e)
        await asyncio.sleep(5)

# ignora SIGTERM/SIGINT para Railway não matar antes da hora
for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, signal.SIG_IGN)

bot.run(TOKEN)# ---------- start (único "run") ----------
