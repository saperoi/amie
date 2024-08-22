import lightbulb
import common
import math
import hikari
import sqlite3

plugin = lightbulb.Plugin('info', 'Useful stuff')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.set_help("Checks latency time in ms")
@lightbulb.command("ping", "Says pong!")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context):
    common.log_com(ctx)
    await common.send_msg(ctx,"Pong! 🏓\t\tIt took " + str(math.floor(1000*plugin.bot.heartbeat_latency)) + " ms to arrive")

@plugin.command
@lightbulb.set_help("Checks if the bot is functioning (sees command and can reply)")
@lightbulb.command("check", "For debugging")
@lightbulb.implements(lightbulb.PrefixCommand)
async def check(ctx: lightbulb.Context):
    common.log_com(ctx)
    await common.send_msg(ctx,"Was registered and could send message")
    print("Sent")

@plugin.command
@lightbulb.option("snowflake", "The snowflake to get the date of.", type=int)
@lightbulb.set_help("Discord snowflakes are in milliseconds starting from 1 January 2015 00:00 UTC+0. Results provided in YYYY-MM-DD")
@lightbulb.command("snowflake", "Pulls information about a snowflake", aliases=["SNOWFLAKE"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def snowflake(ctx: lightbulb.Context):
    common.log_com(ctx)
    description = ""
    description += "**Date**: " + str(hikari.Snowflake(ctx.options.snowflake).created_at)
    embed = hikari.Embed(title=str(ctx.options.snowflake), description=description, color=common.color())
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

@plugin.command
@lightbulb.command("cookie", "Shows the official count of cookies Sapero has! And give them one more!", aliases=["cookies", "cookie_count", "COOKIE", "COOKIE_COUNT", "COOKIES"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def cookie(ctx: lightbulb.Context):
    common.log_com(ctx)
    conmisc = sqlite3.connect("./db/misc.db")
    curmisc = conmisc.cursor()
    curmisc.execute("SELECT value FROM misc_vars WHERE key=?", ("cookies", ) )
    cookie_count, = curmisc.fetchone()
    conmisc.commit()
    await ctx.respond(":cookie: !!! <@738772518441320460>'s cookie count is now " + cookie_count + "!!! :cookie:")
