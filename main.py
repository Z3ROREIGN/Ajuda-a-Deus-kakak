import discord, asyncio, os, signal

TOKEN   = os.environ["TOKEN"]        # seu token de usuário
GUILD   = int(os.environ["GUILD"])
CHANNEL = int(os.environ["CHANNEL"])

intents = discord.Intents.all()
client  = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild   = client.get_guild(GUILD)
    channel = guild.get_channel(CHANNEL)
    while True:
        try:
            vc = await channel.connect()
            print("✅ Entrei na call com minha conta")
            while vc.is_connected():
                await asyncio.sleep(30)
        except Exception as e:
            print(f"❌ Erro: {e} — Reconectando...")
            await asyncio.sleep(3)

for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, signal.SIG_IGN)

client.run(TOKEN)
