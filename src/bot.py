import discord
import multiprocessing

from discord.ext import commands, tasks
from src.config import config

class Bot:
    def __init__(self, server_manager):
        self.server_manager = server_manager
        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix="!", intents=self.intents)
        self.add_commands()

    def run(self):
        self.bot.run(
            config.discord_token
        )

    def start(self):
        multiprocessing.Process(target=self.run, args=()).start()

    def add_commands(self):
        @tasks.loop(seconds=1)
        async def update():
            channel = self.bot.get_channel(1216381943529341101)
            while not self.server_manager.message_queue.empty():
                message = self.server_manager.message_queue.get()
                await channel.send(message)

        @self.bot.event
        async def on_ready():
            await self.bot.tree.sync()
            await update.start()

        @self.bot.tree.command(name="stats", description="Display honeypot stats!")
        async def slash_command(interaction: discord.Interaction):
            await interaction.response.send_message("Stats: wooo")
