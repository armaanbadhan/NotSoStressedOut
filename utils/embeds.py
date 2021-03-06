import discord
import datetime
import humanfriendly

IST = datetime.timedelta(hours=5, minutes=30)


def e_contests(contests: list) -> discord.Embed:
    embed = discord.Embed(color=0x7289DA)
    cnt = 1
    for contest in contests:
        start_end_time = datetime.datetime.strptime(contest[3][:-5], '%Y-%m-%dT%H:%M:%S')
        if contest[4] == -1:
            left_time = start_end_time - datetime.datetime.now()
            embed.add_field(
                name=f"**{cnt}) {contest[0]} {contest[1]}**",
                value=f"End Time: {start_end_time.strftime('%d %B %Y %H:%M')}\n" +
                      f"Time Left: {humanfriendly.format_timespan(left_time.total_seconds())}\n" +
                      f"[LINK]({contest[2]})",
                inline=False
            )
        else:
            start_end_time += IST
            embed.add_field(
                name=f"**{cnt}) {contest[0]} {contest[1]}**",
                value=f"Start Time: {start_end_time.strftime('%d %B %Y %H:%M')}\n" +
                      f"Duration: {humanfriendly.format_timespan(float(contest[4]))}\n" +
                      f"[LINK]({contest[2]})",
                inline=False
            )
        cnt += 1
    return embed
