import discord
from redbot.core import commands

class Echo(commands.Cog):
    """A cog for echoing messages to specified channels."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, channel_id: int, *, message: str):
        """Echo a message to a specified channel."""
        channel = self.bot.get_channel(channel_id)
        if not channel:
            await ctx.send(f"Channel with ID {channel_id} not found.")
            return
        
        await channel.send(message)
        await ctx.send(f"Message echoed to <#{channel_id}>.")

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

def setup(bot):
    bot.add_cog(Echo(bot))
