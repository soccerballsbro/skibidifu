import discord
from discord.ext import commands

class Ping(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Checks the bot's latency.")
    async def ping(self, ctx):
        # FIX 1: Use 'ctx.bot' instead of 'self.bot'. 
        # This is more stable and prevents the Attribute Error.
        latency = round(ctx.bot.latency * 1000)
