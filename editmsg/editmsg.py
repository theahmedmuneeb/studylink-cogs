from redbot.core import commands  # RedBot command framework
from discord import TextChannel, Message  # Discord channel and message types

class EditMessage(commands.Cog):
    """Cog for editing bot messages."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.admin_or_permissions(administrator=True)
    async def editmsg(self, ctx, channel: TextChannel, message_id: int, *, new_text: str):
        """
        Edit a message sent by the bot.
        Usage: !editmsg <channel> <message_id> <new_text>
        """
        try:
            # Fetch the specified message
            message: Message = await channel.fetch_message(message_id)

            # Check if the bot authored the message
            if message.author != self.bot.user:
                return await ctx.send("I can only edit messages that I sent!")

            # Edit the message content
            await message.edit(content=new_text)
            await ctx.send(f"Message edited successfully in {channel.mention}. ✅")

        except Exception as e:
            # Handle any errors and inform the user
            await ctx.send(f"⚠️ An error occurred: {e}")

def setup(bot):
    """Required for the cog to be loaded by RedBot."""
    bot.add_cog(EditMessage(bot))
