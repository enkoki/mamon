from discord.ext import commands
import time

def get_uptime(bot: commands.Bot):
        seconds = int(time.time() - bot.start_time)
        
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        return f"{days} days {hours} hours {minutes} minutes {seconds} seconds"