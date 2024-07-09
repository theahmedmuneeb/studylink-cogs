import discord
from redbot.core import commands

class Echo(commands.Cog):
    """A cog for echoing messages to specified channels."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, channel_input: str = None, message_id: int = None, *, message: str):
        """Echo a message to a specified channel or reply to a message."""
        # Determine the channel to send/reply message
        channel = None
        
        if channel_input:
            channel = await self.get_channel(ctx, channel_input)

        if not channel and message_id:
            try:
                msg = await ctx.channel.fetch_message(message_id)
                await msg.reply(message)
                return
            except discord.NotFound:
                pass

        if not channel and message:
            await ctx.send(message)
        elif channel and message_id:
            try:
                msg = await channel.fetch_message(message_id)
                await msg.reply(message)
            except discord.NotFound:
                await ctx.send(f"Message with ID {message_id} not found in {channel.mention}. Sending message to {channel.mention}.")
                await channel.send(message)
        elif channel:
            await channel.send(message)
        else:
            await ctx.send("Invalid usage. Use `-echo <message> [<channel_id>] [<message_id>]`.")

    async def get_channel(self, ctx, channel_input):
        """Helper function to get channel object from input."""
        if channel_input.startswith("<#") and channel_input.endswith(">"):
            channel_id = int(channel_input[2:-1])
            channel = ctx.guild.get_channel(channel_id)
        else:
            try:
                channel_id = int(channel_input)
                channel = ctx.guild.get_channel(channel_id)
            except ValueError:
                channel = None
        
        return channel

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.")

def setup(bot):
    bot.add_cog(Echo(bot))
