import discord
import datetime
import humanfriendly

IST = datetime.timedelta(hours=5, minutes=30)


def e_contests(contests: list) -> discord.Embed:
    embed = discord.Embed(color=0x7289DA)
    for contest in contests:
        start_time = datetime.datetime.strptime(contest[3][:-5], '%Y-%m-%dT%H:%M:%S') + IST
        embed.add_field(
            name=f"**{contest[1]}**",
            value=f"Start Time: {start_time.strftime('%d %B %Y %H:%M')}\n" +
                  f"Duration = {humanfriendly.format_timespan(float(contest[4]))}\n" +
                  f"[LINK]({contest[2]})",
            inline=False
        )
    return embed
