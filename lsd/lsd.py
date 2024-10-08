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
        """Add the specified role to a user and welcome them."""
        if not await self.has_permission(ctx):
            return
        
        role_id = await self.config.guild(ctx.guild).role()
        role = ctx.guild.get_role(role_id)
        
        if role is None:
            await ctx.send("Role is not set.")
            return

        await member.add_roles(role)
        await ctx.send(f"Welcome {member.mention}!")
        

    @commands.command()
    @commands.guild_only()
    async def lsdrole(self, ctx, role: discord.Role):
        """Set the role to be managed by this cog."""
        if not await self.has_permission(ctx):
            return
        
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Role `{role.name}` has been set.")
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def lsdlist(self, ctx):
        """List all users with the specified role."""
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

    @commands.command()
    @commands.guild_only()
    async def lsdguru(self, ctx, member: discord.Member):
        """Add a user who can use the commands."""
        if not ctx.author.guild_permissions.administrator:
            return

        async with self.config.guild(ctx.guild).guru() as gurus:
            if member.id not in gurus:
                gurus.append(member.id)
                await ctx.send(f"{member.mention} has been added as a guru.")
            else:
                await ctx.send(f"{member.mention} is already a guru.")
        
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def lsdx(self, ctx, member: discord.Member):
        """Remove the specified role from a user."""
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

    @commands.command()
    @commands.guild_only()
    async def lsdgurux(self, ctx, member: discord.Member):
        """Remove a user from the guru list."""
        if not ctx.author.guild_permissions.administrator:
            return

        async with self.config.guild(ctx.guild).guru() as gurus:
            if member.id in gurus:
                gurus.remove(member.id)
                await ctx.send(f"{member.mention} has been removed from the guru list.")
            else:
                await ctx.send(f"{member.mention} is not a guru.")
        
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def lsdgurulist(self, ctx):
        """List all users in the guru list."""
        if not ctx.author.guild_permissions.administrator:
            return

        gurus = await self.config.guild(ctx.guild).guru()
        members = [ctx.guild.get_member(guru_id).mention for guru_id in gurus if ctx.guild.get_member(guru_id)]

        embed = discord.Embed(title="Guru List", description="\n".join(members) or "None", color=discord.Color.green())
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(LSD(bot))
