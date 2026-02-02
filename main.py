import discord
import os
import difflib
from discord.ext import commands

# Your preferred prefixes
prefixes = ["$", "%", "&"]

class MyBot(commands.Bot):
    def __init__(self):
        # Intents.all() allows the bot to see members and messages for prefixes
        intents = discord.Intents.all()
        
        # help_command=None disables the default help menu so your custom cog works
        super().__init__(command_prefix=prefixes, intents=intents, help_command=None)
        
        # Your Centralized Color Palette
        self.colors = {
            "primary": 0x3498db,   # Blue
            "success": 0x2ecc71,   # Green
            "error": 0xe74c3c,     # Red
            "warning": 0xf1c40f,   # Yellow
            "invisible": 0x2b2d31  # Matches Discord Dark Mode
        }

    async def setup_hook(self):
        print("--- Loading Extensions ---")
        # Ensure the cogs directory exists so it doesn't crash
        if not os.path.exists('./cogs'):
            os.makedirs('./cogs')
            
        # Loop through your cogs folder and load every .py file
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✅ Loaded: {filename}')
                except Exception as e:
                    print(f'❌ Failed to load {filename}: {e}')
        
        # Syncs slash commands (if you add any later)
        await self.tree.sync()

    async def on_ready(self):
        # Set the custom status
        await self.change_presence(
            activity=discord.CustomActivity(name=f"🤩 Use {prefixes[0]}help | Moderation And Fun Bot :p"),
            status=discord.Status.online
        )
        print(f'--- {self.user.name} is Online ---')

    # --- THE "DID YOU MEAN" & ERROR LOGIC ---
    async def on_command_error(self, ctx, error):
        # 1. Handle Unknown Commands (Fuzzy Matching)
        if isinstance(error, commands.CommandNotFound):
            # Get list of all available command names
            cmd_names = [cmd.name for cmd in self.commands if not cmd.hidden]
            actual_input = ctx.invoked_with
            
            # Find the closest matches (cutoff 0.4 is the sweet spot)
            matches = difflib.get_close_matches(actual_input, cmd_names, n=3, cutoff=0.4)
            
            embed = discord.Embed(color=self.colors['error'])
            if matches:
                suggestions = ", ".join([f"`{ctx.prefix}{m}`" for m in matches])
                embed.description = f"❌ The Command `{ctx.prefix}{actual_input}` Does Not Exist.\n\nDid You Mean: {suggestions}?"
            else:
                embed.description = f"❌ The Command `{ctx.prefix}{actual_input}` does not exist."
            
            await ctx.reply(embed=embed, mention_author=True)
        
        # 2. Handle Missing Arguments (e.g. $ship with no mentions)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"⚠️ Missing argument: `{error.param.name}`\nUse `{ctx.prefix}help {ctx.command}` to see the correct usage.",
                color=self.colors['warning']
            )
            await ctx.reply(embed=embed, mention_author=True)
            
        # 3. Log other errors to the console so you can see them on Railway
        else:
            print(f"Ignored error in command {ctx.command}: {error}")

# Initialize the bot
bot = MyBot()

# Fetch token from Railway environment variables
token = os.getenv('DISCORD_TOKEN')

if token:
    bot.run(token)
else:
    print("❌ ERROR: No DISCORD_TOKEN found in environment variables!")
