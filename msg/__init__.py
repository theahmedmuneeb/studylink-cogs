from .msg import SendDM
async def setup(bot):
    await bot.add_cog(SendDM(bot))
