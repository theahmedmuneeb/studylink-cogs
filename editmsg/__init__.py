from .editmsg import EditMessage
async def setup(bot):
    await bot.add_cog(EditMessage(bot))
