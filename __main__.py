import discord_slash
import os
from discord.ext import commands
from token import token

bot = commands.Bot(
    command_prefix="[]<>",
    case_insensitive=True,
    when_mentioned=True
)
slash = discord_slash.SlashCommand(bot, sync_commands=True)

print("Initializing...")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("missing perms")
        return
    if isinstance(error, commands.CheckAnyFailure):
        await ctx.send("missing role")
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send("owner only command")
        return
    print(error)


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"**Loaded {extension}**")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"**Unloaded {extension}**")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"**Reloaded {extension}**")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


if __name__ == "__main__":
    bot.run(token)
