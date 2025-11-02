#!/usr/bin/env python3
import os, gc, asyncio, signal, time, psutil
import discord, aiohttp
from discord.ext import commands

TOKEN       = os.getenv("TOKEN")
GUILD_ID    = int(os.getenv("GUILD_ID"))
CHANNEL_ID  = int(os.getenv("CHANNEL"))

# --------- config ultra light ---------------
PREFIX = "!"
intents = discord.Intents.none()
intents.guilds        = True
intents.voice_states  = True   # só precisa disso pra entrar no canal
intents.messages      = True   # responde comandos
# -------------------------------------------

class HardcoreBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            self_bot=True,
            intents=intents,
            heartbeat_timeout=30,
            max_messages=None          # = sem cache
        )
        self.arena_session = None
        # Shutdown graciosa
        signal.signal(signal.SIGTERM, self._die)

    # ---------- 1) anti-flood heartbeat ----------
    async def on_error(self, event, *args, **kwargs):
        # silencia qualquer exceção e continua
        return

    async def on_command_error(self, ctx, error):
        return

    # ---------- 2) cleaner memória ----------
    async def gc_loop(self):
        while True:
            gc.collect(2)
            mem = psutil.Process().memory_info().rss // 1024 // 1024
            print(f"[MEM] {mem} MB")
            await asyncio.sleep(30)

    # ---------- 3) keep-alive voice ----------
    async def stay_vc(self):
        await self.wait_until_ready()
        guild   = self.get_guild(GUILD_ID)
        channel = guild and guild.get_channel(CHANNEL_ID)
        if not channel: return
        while True:
            try:
                vc = guild.voice_client
                if not vc or not vc.is_connected():
                    vc = await channel.connect(timeout=5, reconnect=True)
                # tocando "silêncio" a cada 4 s reinicia o heartbeat
                if not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio(
                        "anullsrc=channel_layout=stereo:sample_rate=48000",  # stream vazia
                        options="-loglevel fatal -vn -f lavfi"
                    ))
                    await asyncio.sleep(0.2)
                    vc.stop()
            except Exception as e:
                print("VC keep:", e)
                await asyncio.sleep(5)
            await asyncio.sleep(4)

    # ---------- 4) desconectar limpo ----------
    async def close(self):
        for vc in self.voice_clients:
            try: await vc.disconnect(force=True)
            except: pass
        await super().close()

    def _die(self, *_):
        asyncio.create_task(self.close())

bot = HardcoreBot()

@bot.event
async def on_ready():
    print(f"{bot.user} ON — RAM {psutil.Process().memory_info().rss//1024//1024} MB")
    bot.loop.create_task(bot.stay_vc())
    bot.loop.create_task(bot.gc_loop())

# --------- 5) sem cache de mensagens ----------
@bot.event
async def on_message(msg):
    # processa comando e já esquece
    await bot.process_commands(msg)
    del msg

# --------- 6) comando !ping para provar vida ----------
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")

if __name__ == "__main__":
    while True:   # loop externo auto-reconecta socket
        try:
            bot.run(TOKEN, bot=False, reconnect=True)
        except (aiohttp.ClientError, discord.GatewayNotFound, discord.ConnectionClosed):
            print("Socket dead — aguarda 10 s")
            time.sleep(10)
