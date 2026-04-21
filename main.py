import discord
from config import BOT_TOKEN

class Client(discord.Client):
    async def on_ready(self):
        print(f'Successfull! Logged on as {self.user}!')
        

intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)
client.run(BOT_TOKEN)