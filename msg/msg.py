from redbot.core import commands
from discord.ext import commands as ext_commands
from discord import utils

class SendDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="msg")
    async def send_dm(self, ctx, user: str, message_id: int = None, *, message: str):
        # Resolve user
        user = await self.resolve_user(ctx, user)
        if not user:
            await ctx.send("User not found.")
            return

        # Process custom tags
        message = self.process_custom_tags(message)
        
        try:
            # Send the message to the user without replying to the original message
            await user.send(message)
            await ctx.send(f"Message sent to {user}.")
        except Exception as e:
            await ctx.send(f"Failed to send message: {str(e)}")

    async def resolve_user(self, ctx, user_identifier: str):
        # Check for mention
        if user_identifier.startswith("<@") and user_identifier.endswith(">"):
            user_id = int(user_identifier[2:-1])
            user = self.bot.get_user(user_id)
            if user:
                return user

        # Check for ID
        try:
            user_id = int(user_identifier)
            user = self.bot.get_user(user_id)
            if user:
                return user
        except ValueError:
            pass

        # Check for username
        user = utils.find(lambda u: str(u) == user_identifier, self.bot.users)
        return user

    def process_custom_tags(self, message: str) -> str:
        import re
        # Replace [{ }] with < >
        message = re.sub(r'\[\{(.*?)\}\]', r'<\1>', message)
        return message

def setup(bot):
    bot.add_cog(SendDM(bot))
