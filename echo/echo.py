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
        # Split args by first two spaces to separate message, channel_id, and message_id
        try:
            message, rest = args.split(maxsplit=1)
            rest = rest.split(maxsplit=2)
        except ValueError:
            message = args
            rest = []

        if not rest:
            channel = ctx.channel
        elif len(rest) == 1:
            channel = await self.get_channel(ctx, rest[0])
            message = None
        else:
            channel = await self.get_channel(ctx, rest[0])
            message_id = rest[1]

        if message:
            if channel:
                if message_id:
                    try:
                        message_id = int(message_id)
                        msg = await channel.fetch_message(message_id)
                        await msg.reply(message)
                    except ValueError:
                        await ctx.send("Invalid message ID provided.")
                else:
                    await channel.send(message.strip())
            else:
                await ctx.send("Channel not found.")
        else:
            await ctx.send("No message provided.")

    async def get_channel(self, ctx, channel_input):
        """Helper function to get channel object from input."""
        # Check if channel_input is a channel mention
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
