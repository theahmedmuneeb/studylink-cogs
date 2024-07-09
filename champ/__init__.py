from .champ import Champ
async def setup(bot):
    await bot.add_cog(Champ(bot))
