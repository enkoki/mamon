import discord
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged In Successfully! Online as: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('bye'):
        await message.channel.send(f"Goodbye, {message.author}")

if __name__ == '__main__':
    bot.run(BOT_TOKEN)