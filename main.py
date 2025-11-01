import discord, asyncio, os, signal

TOKEN   = os.environ["TOKEN"]          # variável no painel
GUILD   = int(os.environ["GUILD"])     # variável no painel
CHANNEL = int(os.environ["CHANNEL"])   # variável no painel

intents = discord.Intents.all()
client  = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild   = client.get_guild(GUILD)
    channel = guild.get_channel(CHANNEL)
    while True:
        try:
            vc = await channel.connect(reconnect=True, timeout=5)
            print("🎙️ Conectado na call")
            while vc.is_connected():
                await asyncio.sleep(30)
        except Exception as e:
            print(f"❌ Erro: {e} — Reconectando...")
            await asyncio.sleep(3)

# ignora Ctrl+C dentro do container
for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, signal.SIG_IGN)

client.run(TOKEN)
