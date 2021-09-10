import os
import pytz
import json
import discord
import datetime
import discord_slash
import discord.ext.commands as commands

from cloudant import Cloudant
from config import TOKEN, LOGGING_CHANNEL_ID, scheduler
from utils import embeds, get_data, flask_thing
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_button, spread_to_rows, ComponentContext
from apscheduler.jobstores.base import ConflictingIdError

bot = commands.Bot(command_prefix="@#$%(*&^%")
slash = discord_slash.SlashCommand(bot, sync_commands=True)

print("Initializing...")

db_name = 'mydb'
client = None
db = None


if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    logging_channel = await bot.fetch_channel(LOGGING_CHANNEL_ID)
    await logging_channel.send("logged in")


@bot.event
async def on_command_error(ctx, error):
    desc = f"```{ctx.message.content}\n{error}```"
    logging_channel = await bot.fetch_channel(LOGGING_CHANNEL_ID)
    await logging_channel.send(desc)


@bot.event
async def on_slash_command_error(ctx, error):
    desc = f"```error on /{ctx.name}\n{error}```"
    logging_channel = await bot.fetch_channel(LOGGING_CHANNEL_ID)
    await logging_channel.send(desc)


@bot.event
async def on_component(ctx: ComponentContext):
    contest_name, start_time = str(ctx.custom_id).split(";")
    start_time_dt = datetime.datetime.strptime(start_time[:-5], '%Y-%m-%dT%H:%M:%S')
    if start_time_dt < datetime.datetime.now() + datetime.timedelta(hours=1):
        await ctx.send(f"less then one hour left for contest!", hidden=True)
        return
    start_time_dt += datetime.timedelta(hours=5, minutes=30)       # to ist
    start_time_dt -= datetime.timedelta(hours=1)                   # 1 hour reminder
    try:
        scheduler.add_job(
            func=send_to_discord,
            trigger="cron",
            id=f"{ctx.channel_id};{ctx.author_id};{contest_name}",
            year=start_time_dt.year,
            month=start_time_dt.month,
            day=start_time_dt.day,
            hour=start_time_dt.hour,
            minute=start_time_dt.minute,
            second=start_time_dt.second,
            timezone=pytz.timezone("Asia/Kolkata"),
            kwargs={
                "channel_id": ctx.channel_id,
                "contest_name": contest_name,
                "user_id": ctx.author_id,
            }
        )
    except ConflictingIdError:
        await ctx.send("Reminder already exists", hidden=True)
        return
    await ctx.send(f"{ctx.author}:\nreminder set successfully for {contest_name}")


@slash.slash(
    name="upcoming_contests",
    description="check out the upcoming contests",
    options=[
        create_option(
            name="online_judge",
            description="name of the online judge",
            option_type=3,
            required=True,
            choices=[create_choice(name=i, value=i) for i in get_data.URLS]
        )
    ]
)
async def upcoming(ctx, online_judge: discord_slash.SlashContext):
    await ctx.defer()
    contests = get_data.get_contests(str(online_judge))[1]
    if contests:
        buttons = [
            create_button(
                style=ButtonStyle.blue,
                label=f"  {x}  ",
                custom_id=f"{contests[x - 1][1]};{contests[x - 1][3]}"
            ) for x in range(1, len(contests) + 1)
        ]
        rows = spread_to_rows(*buttons)
        await ctx.send("**CLICK ON THE BUTTON TO SET REMINDER**", embed=embeds.e_contests(contests), components=rows)
    else:
        await ctx.send("no upcoming contests found")


@slash.slash(
    name="running_contests",
    description="check out the running contests",
    options=[
        create_option(
            name="online_judge",
            description="name of the online judge",
            option_type=3,
            required=True,
            choices=[create_choice(name=i, value=i) for i in get_data.URLS]
        )
    ]
)
async def running(ctx, online_judge: discord_slash.SlashContext):
    await ctx.defer()
    contests = get_data.get_contests(str(online_judge))[0]
    if contests:
        await ctx.send(embed=embeds.e_contests(contests))
    else:
        await ctx.send("no running contests found")


@slash.slash(
    name="next_24_hours",
    description="check out the contests in next 24 hours",
)
async def next_twentyfourhours_slash(ctx):
    await ctx.defer()
    contests = get_data.in_24_hours()
    if contests:
        buttons = [
            create_button(
                style=ButtonStyle.blue, 
                label=f"  {x}  ",
                custom_id=f"{contests[x-1][1]};{contests[x-1][3]}"
            ) for x in range(1, len(contests) + 1)
        ]
        rows = spread_to_rows(*buttons)
        await ctx.send("**CLICK ON THE BUTTON TO SET REMINDER**", embed=embeds.e_contests(contests), components=rows)
    else:
        await ctx.send("no contests in next 24 hours")


async def send_to_discord(channel_id: int, contest_name: str, user_id: int):
    channel = bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title=contest_name,
            description="Starts in 20 minutes",
            colour=0xff0000
        )
        await channel.send(f"<@!{user_id}>", embed=embed)


@scheduler.scheduled_job("interval", hours=12, start_date='2021-10-10 10:00:00')
async def send_24hrs_contests_discord():
    contests = get_data.in_24_hours()
    if contests:
        channel = bot.get_channel(864017066901504030)
        buttons = [
            create_button(
                style=ButtonStyle.blue,
                label=f"  {x}  ",
                custom_id=f"{contests[x - 1][1]};{contests[x - 1][3]}"
            ) for x in range(1, len(contests) + 1)
        ]
        rows = spread_to_rows(*buttons)
        await channel.send(
            "**CONTESTS IN NEXT 24 HOURS\nCLICK ON THE BUTTON TO SET REMINDER**",
            embed=embeds.e_contests(contests),
            components=rows
        )


def start():
    flask_thing.keep_alive()
    scheduler.start()
    bot.run(TOKEN)


if __name__ == "__main__":
    start()
