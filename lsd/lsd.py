import discord
from discord.ext import commands
from redbot.core import commands, Config, checks

class LSD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_guild(role=None, guru=[])

    async def has_permission(self, ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        gurus = await self.config.guild(ctx.guild).guru()
        return ctx.author.id in gurus

    @commands.command()
    @commands.guild_only()
    async def lsd(self, ctx, member: discord.Member):
        if not await self.has_permission(ctx):
            return
        
        role_id = await self.config.guild(ctx.guild).role()
        role = ctx.guild.get_role(role_id)
        
        if role is None:
            await ctx.send("Role is not set.")
            return

        await member.add_roles(role)
        await ctx.message.delete()

    @lsd.group()
    async def role(self, ctx, role: discord.Role):
        if not await self.has_permission(ctx):
            return
        
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Role `{role.name}` has been set.")
        await ctx.message.delete()

    @lsd.command()
    async def list(self, ctx):
        if not await self.has_permission(ctx):
            return
        
        role_id = await self.config.guild(ctx.guild).role()
        role = ctx.guild.get_role(role_id)

        if role is None:
            await ctx.send("Role is not set.")
            return

        members = [member.mention for member in ctx.guild.members if role in member.roles]
        
        embed = discord.Embed(title=f"Users with the `{role.name}` role", description="\n".join(members) or "None", color=discord.Color.blue())
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @lsd.command()
    async def guru(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.administrator:
            return

        async with self.config.guild(ctx.guild).guru() as gurus:
            if member.id not in gurus:
                gurus.append(member.id)
                await ctx.send(f"{member.mention} has been added as a guru.")
            else:
                await ctx.send(f"{member.mention} is already a guru.")
        
        await ctx.message.delete()

    @lsd.command()
    async def x(self, ctx, member: discord.Member):
        if not await self.has_permission(ctx):
            return
        
        role_id = await self.config.guild(ctx.guild).role()
        role = ctx.guild.get_role(role_id)

        if role is None:
            await ctx.send("Role is not set.")
            return

        await member.remove_roles(role)
        await ctx.send(f"Role `{role.name}` has been removed from {member.mention}.")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(LSD(bot))
