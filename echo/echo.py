import discord
from redbot.core import commands
import re

class Echo(commands.Cog):
    """A cog for echoing messages to specified channels."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, channel_input: str = None, message_id: int = None, *, message: str):
        """Echo a message to a specified channel or reply to a message.
        
        Usage: -echo [- | <channel_id> | #channel | [{channel_id}]] [<message_id>] <message>
        """
        if channel_input == "-":
            channel = ctx.channel
        else:
            channel = await self.get_channel(ctx, channel_input)

        # Format the message to replace custom emoji syntax
        formatted_message = self.format_message(message)

        if not channel and message_id:
            try:
                msg = await ctx.channel.fetch_message(message_id)
                await msg.reply(formatted_message, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))
                return
            except discord.NotFound:
                pass

        if not channel and formatted_message:
            await ctx.send(formatted_message, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))
        elif channel and message_id:
            try:
                msg = await channel.fetch_message(message_id)
                await msg.reply(formatted_message, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))
            except discord.NotFound:
                await ctx.send(f"Message with ID {message_id} not found in {channel.mention}. Sending message to {channel.mention}.")
                await channel.send(formatted_message, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))
        elif channel:
            await channel.send(formatted_message, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))
        else:
            await ctx.send("Invalid usage. Use `-echo [- | <channel_id> | #channel | [{channel_id}]] [<message_id>] <message>`.")

    async def get_channel(self, ctx, channel_input):
        """Helper function to get channel object from input."""
        if channel_input.startswith("<#") and channel_input.endswith(">"):
            channel_id = int(channel_input[2:-1])
            channel = ctx.guild.get_channel(channel_id)
        elif channel_input.startswith("[{") and channel_input.endswith("}]"):
            channel_id = int(channel_input[2:-2])
            channel = ctx.guild.get_channel(channel_id)
        elif channel_input.isdigit():
            try:
                channel_id = int(channel_input)
                channel = ctx.guild.get_channel(channel_id)
            except ValueError:
                channel = None
        else:
            channel = None
        
        return channel

    def format_message(self, message):
        """Helper function to format custom emoji syntax in the message."""
        # Replace [{;emojiname; emojiid}] with <:emojiname:emojiid>
        custom_emoji_pattern = re.compile(r"\[\{;(.*?); (\d+);}]")
        def replace_emoji(match):
            emoji_name = match.group(1)
            emoji_id = match.group(2)
            return f"<:{emoji_name}:{emoji_id}>"
        
        formatted_message = custom_emoji_pattern.sub(replace_emoji, message)
        
        return formatted_message

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.")

def setup(bot):
    bot.add_cog(Echo(bot))
