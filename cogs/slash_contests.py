from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import utils.get_data
from utils.embeds import e_contests

guild_ids = [798268746744594465]


class AddStuffSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="upcoming_contests",
        guild_ids=guild_ids,
        description="check out the upcoming contests",
        options=[
            create_option(
                name="online_judge",
                description="name of the online judge",
                option_type=3,
                required=True,
                choices=[create_choice(name=i, value=i) for i in utils.get_data.URLS]
            )
        ]
    )
    async def upcoming(self, ctx, online_judge: SlashContext):
        await ctx.defer()
        contests = utils.get_data.get_contests(str(online_judge))[1]
        if contests:
            await ctx.send(embed=e_contests(contests))
        else:
            await ctx.send("no upcoming contests found")

    @cog_ext.cog_slash(
        name="running_contests",
        guild_ids=guild_ids,
        description="check out the running contests",
        options=[
            create_option(
                name="online_judge",
                description="name of the online judge",
                option_type=3,
                required=True,
                choices=[create_choice(name=i, value=i) for i in utils.get_data.URLS]
            )
        ]
    )
    async def running(self, ctx, online_judge: SlashContext):
        await ctx.defer()
        contests = utils.get_data.get_contests(str(online_judge))[0]
        if contests:
            await ctx.send(embed=e_contests(contests))
        else:
            await ctx.send("no running contests found")

    @cog_ext.cog_slash(
        name="next_24_hours",
        guild_ids=guild_ids,
        description="check out the contests in next 24 hours",
    )
    async def next_twentyfourhours_slash(self, ctx):
        await ctx.defer()
        contests = utils.get_data.in_24_hours()
        if contests:
            await ctx.send(embed=e_contests(contests))
        else:
            await ctx.send("no contests in next 24 hours")


def setup(bot):
    bot.add_cog(AddStuffSlash(bot))
