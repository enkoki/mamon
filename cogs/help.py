import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID
from settings import BOT_NAME, DEFAULT_COLOR
from datetime import datetime

COMMANDS_PER_PAGE = 10


class HelpView(discord.ui.View):
    def __init__(self, pages: list[discord.Embed]):
        super().__init__(timeout=60)
        self.pages = pages
        self.current = 0
        self._update_buttons()

    def _update_buttons(self):
        self.prev_button.disabled = self.current == 0
        self.next_button.disabled = self.current == len(self.pages) - 1

    @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.secondary)
    async def prev_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        self.current -= 1
        self._update_buttons()
        await interaction.response.edit_message(
            embed=self.pages[self.current],
            view=self,
        )

    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.secondary)
    async def next_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        self.current += 1
        self._update_buttons()
        await interaction.response.edit_message(
            embed=self.pages[self.current],
            view=self,
        )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help",description="See all available commands",)
    async def _help(self, interaction: discord.Interaction):
        commands_list = sorted(
            # self.bot.tree.get_commands(guild=GUILD_ID),
            self.bot.tree.get_commands(),
            key=lambda c: c.name,
        )

        total = len(commands_list)

        chunks = [
            commands_list[i:i + COMMANDS_PER_PAGE]
            for i in range(0, total, COMMANDS_PER_PAGE)
        ]

        total_pages = len(chunks)
        pages = []

        for i, chunk in enumerate(chunks):
            command_text = "\n".join(
                f"> `{cmd.name}` "
                for cmd in chunk
            )

            embed = discord.Embed(
                title=f"{BOT_NAME} Commands",
                description=f"> Use  `/help <command>` to get more information\n\n{command_text}",
                color=discord.Colour.from_str(DEFAULT_COLOR),
                timestamp=datetime.now(),
            )

            # embed.set_thumbnail(url=self.bot.user.display_avatar.url)

            embed.set_footer(text=(f"Page {i + 1}/{total_pages} • "f"{total} commands • "))

            pages.append(embed)

        view = HelpView(pages)
        await interaction.response.send_message(embed=pages[0], view=view, ephemeral=True,)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))