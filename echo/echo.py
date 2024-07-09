import discord
from redbot.core import commands

class Echo(commands.Cog):
    """A cog for echoing messages to specified channels."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, *, args):
        """Echo a message to a specified channel or the current channel."""
        # Split args by spaces
        args = args.split(maxsplit=1)
        
        if len(args) < 2:
            await ctx.send("Invalid usage. Use `-echo <channel> <message>`.")
            return
        
        channel_input, message = args
        
        # Check if channel_input is a channel mention
        if channel_input.startswith("<#") and channel_input.endswith(">"):
            channel_id = int(channel_input[2:-1])
            channel = ctx.guild.get_channel(channel_id)
        else:
            try:
                channel_id = int(channel_input)
                channel = ctx.guild.get_channel(channel_id)
            except ValueError:
                channel = ctx.channel  # Default to current channel
        
        if not channel:
            await ctx.send(f"Channel with ID {channel_id} not found.")
            return
        
        await channel.send(message.strip())

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.")

def setup(bot):
    bot.add_cog(Echo(bot))
