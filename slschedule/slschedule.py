import discord
from redbot.core import commands, Config
from redbot.core.bot import Red
import aiocron
import asyncio

class SLSchedule(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_global = {
            "schedules": {}
        }
        self.config.register_global(**default_global)
        self.crons = {}

    @commands.group()
    async def slschedule(self, ctx):
        """Manage scheduled commands."""
        pass

    @slschedule.command()
    async def add(self, ctx, name: str, time: str, *, command: str):
        """Add a new schedule."""
        schedules = await self.config.schedules()
        if name in schedules:
            await ctx.send("A schedule with this name already exists.")
            return

        schedules[name] = {"time": time, "command": command}
        await self.config.schedules.set(schedules)
        self._create_cron(name, time, command)
        await ctx.send(f"Schedule '{name}' added.")

    @slschedule.command()
    async def list(self, ctx):
        """List all schedules."""
        schedules = await self.config.schedules()
        if not schedules:
            await ctx.send("No schedules found.")
            return

        msg = "Scheduled commands:\n"
        for name, data in schedules.items():
            msg += f"- {name}: Every {data['time']}, Command: {data['command']}\n"
        await ctx.send(msg)

    @slschedule.command()
    async def del(self, ctx, name: str):
        """Delete a schedule."""
        schedules = await self.config.schedules()
        if name not in schedules:
            await ctx.send("No schedule found with this name.")
            return

        del schedules[name]
        await self.config.schedules.set(schedules)
        self._remove_cron(name)
        await ctx.send(f"Schedule '{name}' deleted.")

    @slschedule.command()
    async def edit(self, ctx, name: str, time: str, *, command: str):
        """Edit an existing schedule."""
        schedules = await self.config.schedules()
        if name not in schedules:
            await ctx.send("No schedule found with this name.")
            return

        schedules[name] = {"time": time, "command": command}
        await self.config.schedules.set(schedules)
        self._remove_cron(name)
        self._create_cron(name, time, command)
        await ctx.send(f"Schedule '{name}' edited.")

    def cog_load(self):
        asyncio.create_task(self._load_schedules())

    async def _load_schedules(self):
        await self.bot.wait_until_ready()
        schedules = await self.config.schedules()
        for name, data in schedules.items():
            self._create_cron(name, data["time"], data["command"])

    def _create_cron(self, name, time, command):
        cron = aiocron.crontab(time, func=self._execute_command, args=(command,))
        self.crons[name] = cron

    def _remove_cron(self, name):
        if name in self.crons:
            self.crons[name].stop()
            del self.crons[name]

    async def _execute_command(self, command):
        ctx = await self.bot.get_context(self.bot)
        if command.startswith('/'):
            # Handle slash commands
            slash_command = self.bot.get_slash_command(command[1:])
            if slash_command:
                await slash_command(ctx)
        else:
            # Handle regular commands
            await ctx.invoke(await self.bot.get_command(command))

def setup(bot: Red):
    bot.add_cog(SLSchedule(bot))
