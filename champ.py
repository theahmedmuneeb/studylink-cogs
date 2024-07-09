import discord
from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box

class ChampAnnouncement(commands.Cog):
    """A cog for making announcements."""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_global(default_channel_id=None, default_name="Champion", default_role_id=None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def champ(self, ctx, user_id: int, name: str = None, role_id: int = None, channel_id: int = None):
        """Announce a champion message mentioning a user and a role."""
        user = ctx.guild.get_member(user_id)
        
        # Use provided or default values for name and role_id
        name = name or await self.config.default_name()
        role_id = role_id or await self.config.default_role_id()
        role = ctx.guild.get_role(role_id)
        
        # Use the provided channel ID or the default one
        if channel_id:
            channel = self.bot.get_channel(channel_id)
        else:
            default_channel_id = await self.config.default_channel_id()
            if default_channel_id:
                channel = self.bot.get_channel(default_channel_id)
            else:
                await ctx.send("No channel ID provided and no default channel set.")
                return

        if user and channel and role:
            message = f"{name} champion is {user.mention}, received a role {role.mention}"
            await channel.send(message)
        else:
            await ctx.send("Invalid user ID, role ID, or channel ID.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchampdefaults(self, ctx, name: str, role_id: int, channel_id: int):
        """Set the default name, role ID, and channel ID for announcements."""
        await self.config.default_name.set(name)
        await self.config.default_role_id.set(role_id)
        await self.config.default_channel_id.set(channel_id)
        await ctx.send(f"Default settings updated:\nName: {name}\nRole ID: {role_id}\nChannel ID: {channel_id}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.")

def setup(bot: Red):
    bot.add_cog(ChampAnnouncement(bot))
