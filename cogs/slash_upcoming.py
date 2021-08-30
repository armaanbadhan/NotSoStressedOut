from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from utils.get_data import get_contests
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
                choices=[create_choice(name=i, value=i) for i in ["codechef", "codeforces", "kickstart"]]
            )
        ]
    )
    async def upcoming(self, ctx, online_judge: SlashContext):
        await ctx.defer()
        contests = get_contests(str(online_judge))
        await ctx.send(embed=e_contests(contests))


def setup(bot):
    bot.add_cog(AddStuffSlash(bot))
