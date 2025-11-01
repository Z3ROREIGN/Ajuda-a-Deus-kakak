import os, asyncio, signal, logging, sys
import discord
from discord.ext import tasks

TOKEN   = os.getenv("TOKEN")          # seu token de usuário
GUILD   = int(os.getenv("GUILD"))     # ID do servidor
CHANNEL = int(os.getenv("CHANNEL"))   # ID da call de voz

intents = discord.Intents.all()
client  = discord.Client(intents=intents)

# ---------- helpers ----------
def log(msg):
    print(msg, flush=True)

async def safe_connect():
    guild   = client.get_guild(GUILD)
    if not guild:
        log("❌ Servidor não encontrado."); return None
    channel = guild.get_channel(CHANNEL)
    if not channel or not isinstance(channel, discord.VoiceChannel):
        log("❌ Canal de voz não encontrado."); return None
    try:
        vc = await channel.connect(timeout=5, reconnect=True)
        log("✅ Conectado na call.")
        return vc
    except Exception as e:
        log(f"❌ Falha ao conectar: {e}")
        return None

# ---------- loop infinito ----------
@tasks.loop(seconds=10)
async def watchdog():
    guild   = client.get_guild(GUILD)
    channel = guild.get_channel(CHANNEL) if guild else None
    if not channel: return

    # Se já estiver conectado nessa call, apenas heartbeat
    for vc in client.voice_clients:
        if vc.channel == channel and vc.is_connected():
            return  # tudo certo

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
