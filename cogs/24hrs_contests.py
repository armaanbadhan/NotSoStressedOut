from discord.ext import tasks, commands
from utils.embeds import e_contests
from utils.get_data import in_24_hours


class EventLoopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twenty_four_hour_loop.start()

    def cog_unload(self):
        self.twenty_four_hour_loop.cancel()

    @tasks.loop(seconds=30.0)
    async def twenty_four_hour_loop(self):
        channel = self.bot.get_channel(798458622836867094)
        contests = in_24_hours()
        if contests:
            await channel.send("all contests in next 24 hours", embed=e_contests(contests))

    @twenty_four_hour_loop.before_loop
    async def before_printer(self):
        print(f'waiting for bot to start ({__name__})')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(EventLoopCog(bot))
