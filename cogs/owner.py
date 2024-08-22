import lightbulb
import hikari
import common
import sqlite3

plugin = lightbulb.Plugin('owner', "Owner-only commands")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.add_checks(common.owners_only)
@lightbulb.option("extension_name", "The name of the extension to reload.")
@lightbulb.command("reload", "Reload an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def reload_cmd(ctx: lightbulb.Context):
    common.log_com(ctx)
    ctx.app.reload_extensions("cogs." + ctx.options.extension_name)
    await ctx.respond("Reloaded " + ctx.options.extension_name)

@plugin.command
@lightbulb.add_checks(common.owners_only)
@lightbulb.option("extension_name", "The name of the extension to load.")
@lightbulb.command("load", "Load an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def load_cmd(ctx: lightbulb.Context):
    common.log_com(ctx)
    ctx.app.load_extensions("cogs." + ctx.options.extension_name)
    await ctx.respond("Loaded " + ctx.options.extension_name)

@plugin.command
@lightbulb.add_checks(common.owners_only)
@lightbulb.option("extension_name", "The name of the extension to unload.")
@lightbulb.command("unload", "Unload an extension", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def unload_cmd(ctx: lightbulb.Context):
    common.log_com(ctx)
    ctx.app.unload_extensions("cogs." + ctx.options.extension_name)
    await ctx.respond("Unloaded " + ctx.options.extension_name)

@plugin.command
@lightbulb.add_checks(common.owners_only)
@lightbulb.command("shutdown", "Shuts down the bot", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def shutdown(ctx: lightbulb.Context):
    common.log_com(ctx)
    await ctx.respond("Shutting down...")
    quit()

@plugin.command
@lightbulb.add_checks(common.owners_only)
@lightbulb.command("resetchar", "Resets the character table", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def resetchar(ctx: lightbulb.Context):
    common.log_com(ctx)
    con = sqlite3.connect("./db/char.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS `characters`")
    con.commit()
    tablecommand = """create table `characters` (
  `uid` BIGINT not null,
  `name` varchar(255) not null,
  `essence` INT not null default 0,
  `lastrollstat` varchar(6) not null default 0,
  `lastroll` INT not null default 0,
  `smarts_dice` INT not null default 0,
  `smarts_bonus` INT not null default 0,
  `smarts_magic` INT not null default 0,
  `charm_dice` INT not null default 0,
  `charm_bonus` INT not null default 0,
  `charm_magic` INT not null default 0,
  `grit_dice` INT not null default 0,
  `grit_bonus` INT not null default 0,
  `grit_magic` INT not null default 0,
  `vigor_dice` INT not null default 0,
  `vigor_bonus` INT not null default 0,
  `vigor_magic` INT not null default 0,
  `tussle_dice` INT not null default 0,
  `tussle_bonus` INT not null default 0,
  `tussle_magic` INT not null default 0,
  `flight_dice` INT not null default 0,
  `flight_bonus` INT not null default 0,
  `flight_magic` INT not null default 0
)"""
    cur.execute(tablecommand)
    con.commit()
    await ctx.respond("Successfully reset tables.")