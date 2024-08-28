from .lsd import LSD
async def setup(bot):
    await bot.add_cog(LSD(bot))
