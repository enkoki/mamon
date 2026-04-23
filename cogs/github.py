import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID, OWNER_ID
from datetime import datetime

class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="github", description="Repo link")
    async def github(self, interaction: discord.Interaction):
        owner = await self.bot.fetch_user(OWNER_ID) 
        embed = discord.Embed( 
            title="GitHub Repository | Mamon", 
            url="https://github.com/enkoki/mamon", 
            description=( 
                "A Discord bot built using discord.py, created for learning the basics of bot development. " 
                "This project is currently in early development and is mainly focused on learning and experimenting with Discord bot fundamentals." 
            ), 
            color=discord.Color.from_str("#000000") 
        ) 
        embed.set_thumbnail(url="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.png") 
        embed.add_field( 
            name="Commands", 
            value=( 
                "`/hello`\n" 
                "`/say <text>`\n" 
                "`/github`\n" 
            ), 
            inline = False 
        ) 

        embed.add_field( 
            name="Features",
            value=( 
                "- Leveling\n" 
                "- Moderation\n" 
                "- Logs" 
            ),
            inline=False
        ) 
        embed.set_footer(text="Make sure to Star the Repository!") 
        embed.set_author( 
            name=owner.name, 
            icon_url=owner.display_avatar.url 
        ) 
        embed.set_image(url="https://i.imgur.com/IBrUrab.png") 
        embed.timestamp = datetime.now() 
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Github(bot), guild=GUILD_ID)