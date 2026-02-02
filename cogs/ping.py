import discord
from discord.ext import commands

class Ping(commands.Cog):
    def init(self, bot):
        self.bot = bot

    # 1. 'hybrid_command' enables both Slash (/) and Prefix ($) support
    @commands.hybrid_command(name="ping", description="Checks the bot's latency.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)

        color = self.bot.colors['success'] if latency < 150 else self.bot.colors['error']

        # 2. Simplified Embed: No fields, thumbnails, or footers. Just the data.
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=color
        )

        # ctx.send automatically handles both Slash and Text contexts
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
