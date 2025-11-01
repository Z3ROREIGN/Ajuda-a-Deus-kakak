import os
import asyncio
import discord
from discord.ext import commands

TOKEN   = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL   = int(os.getenv("CHANNEL"))
PREFIX   = "!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, self_bot=True, intents=intents)

@bot.event
async def on_ready():
    bot.loop.create_task(stay_in_vc())

async def stay_in_vc():
    await bot.wait_until_ready()
    guild   = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(VC_ID)
    while True:
        try:
            if not guild.voice_client or not guild.voice_client.is_connected():
                await channel.connect()
        except Exception as e:
            print(e)
        await asyncio.sleep(5)

bot.run(TOKEN)async def join(ctx):
    """Entra no canal de voz do autor."""
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.author.voice.channel.connect()
        await ctx.message.add_reaction("✅")

@bot.command()
async def leave(ctx):
    """Sai do canal de voz."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction("✅")

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("TOKEN não definido.")
    bot.run(TOKEN)
    # Se já estiver conectado nessa call, apenas heartbeat
    for vc in client.voice_clients:
        if vc.channel == channel and vc.is_connected():
            return

    # Senão, reconecta
    log("🔄 Reconectando...")
    await safe_connect()

@client.event
async def on_ready():
    log(f"🤖 Logado como {client.user} ({client.user.id})")
    watchdog.start()          # inicia o loop eterno
    await safe_connect()      # primeira conexão

# ---------- ignora SIGTERM/SIGINT ----------
for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, signal.SIG_IGN)

# ---------- start ----------
client.run(TOKEN)
