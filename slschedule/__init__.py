from .slschedule import SLSchedule
async def setup(bot):
    await bot.add_cog(SLSchedule(bot))
