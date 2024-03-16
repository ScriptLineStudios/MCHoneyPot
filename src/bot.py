import discord
import multiprocessing
import random

from discord.ext import commands, tasks
from src.config import config
from src.database import Database

class Bot:
    QUOTES = [
        "Premature optimisation is the root of all evil", 
        "You are the player. Wake up.", 
        "Reporting scanners since 2024",
        "I eat pings for breakfast", 
        "Try joining me!",
        "I am become honey, catcher of scanners"
    ]
    def __init__(self, server_manager):
        self.server_manager = server_manager
        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix="!", intents=self.intents)
        self.add_commands()
        self.db = Database()

    def run(self):
        self.bot.run(
            config.discord_token
        )

    def start(self):
        multiprocessing.Process(target=self.run, args=()).start()

    def add_commands(self):
        @tasks.loop(seconds=1)
        async def update():
            channel = self.bot.get_channel(1218310329415634995)
            while not self.server_manager.message_queue.empty():
                message = self.server_manager.message_queue.get()
                await channel.send(message)

        @self.bot.event
        async def on_ready():
            await self.bot.tree.sync()
            await update.start()

        @self.bot.tree.command(name="stats", description="Display honeypot stats!")
        async def stats(interaction: discord.Interaction):
            username = self.db.get_latest_join()[0]["name"]
            embed = discord.Embed(title="Statistics", description="Honeypot Statistics", color=discord.Color.red())
            embed.set_author(name="MCHoneyPot")
            embed.add_field(name="Total pings", value=self.db.get_ping_size())
            embed.add_field(name="Total joins", value=self.db.get_join_size())
            embed.add_field(name="Total reports", value=self.db.get_report_size())
            embed.add_field(name="Latest ping", value=self.db.get_latest_ping()[0]["ip"])
            embed.add_field(name="Latest join", value=username)
            embed.set_image(url=f"https://mineskin.eu/avatar/{username}")
            embed.set_footer(text=random.choice(self.QUOTES))

            await interaction.response.send_message(embed=embed)

        @self.bot.tree.command(name="joins", description="Get a list of latest join attempts")
        async def stats(interaction: discord.Interaction):
            joins = list(self.db.get_latest_join(5))
            embeds = []
            for join in joins:
                ping = self.db.ping_collection.find_one({"ip": join["ip"]})
                embed = discord.Embed(title="Join", color=discord.Color.blue())
                embed.set_author(name="MCHoneyPot")
                embed.add_field(name=f"{join['name']}", value=f"{join['ip']}", inline=False)
                embed.add_field(name=f":flag_{ping['country'].lower()}:", value="", inline=False)
                embed.set_thumbnail(url=f"https://mineskin.eu/avatar/{join['name']}")
                embeds.append(embed)

            await interaction.response.send_message(embeds=embeds)