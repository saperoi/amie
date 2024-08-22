import lightbulb
import hikari
import common
import sqlite3
import random

plugin = lightbulb.Plugin('char', 'CHOOSE YOUR CHARACTER!')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

con = sqlite3.connect("./db/char.db")
cur = con.cursor()

def existcharcheck(user, char):
    cur.execute("SELECT COUNT(*) FROM characters WHERE uid=? AND name=?", (user, char))
    return bool(cur.fetchone()[0])

@plugin.command
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("create", "Command to create a character", aliases=["CREATE", "crt", "CRT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def createchar(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.name)
    if existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` already exists")
        return
    cur.execute("INSERT INTO characters (uid, name) VALUES (?, ?)", (ctx.author.id, char))
    con.commit()
    await ctx.respond(f"Character `{char}` created.")

@plugin.command
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("delete", "Command to delete a character", aliases=["DELETE", "dlt", "DLT"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def deletechar(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.name)
    if not existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    cur.execute("DELETE FROM characters WHERE uid=? AND name=?", (ctx.author.id, char))
    con.commit()
    await ctx.respond(f"Successfully deleted character `{char}`")

@plugin.command
@lightbulb.option("newname", "The new name for the character", type=str)
@lightbulb.option("name", "The current name of the character", type=str)
@lightbulb.command("rename", "Command to rename a character", aliases=["RENAME", "rnm", "RNM"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def renamechar(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.name)
    if not existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    nchar = common.clean_name(ctx.options.newname)
    if existcharcheck(ctx.author.id, nchar):
        await ctx.respond(f"Character `{nchar}` already exists")
        return
    cur.execute("UPDATE characters SET name=? WHERE uid=? AND name=?", (nchar, ctx.author.id, char))
    con.commit()
    await ctx.respond(f"Successfully renamed character `{char}` to `{nchar}`")

@plugin.command
@lightbulb.command("list", "Command to list all character", aliases=["LIST", "lst", "LST"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def listchar(ctx: lightbulb.Context):
    common.log_com(ctx)
    cur.execute("SELECT name FROM characters WHERE uid=?", (ctx.author.id,))
    r = [_[0] for _ in cur.fetchall()]
    nl = "\n"
    m = f"Your list of characters:{nl}- `{f'`{nl}- `'.join(r)}`"
    await common.send_msg(ctx, m)

@plugin.command
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("profile", "Command to show the profile of a character", aliases=["PROFILE"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def listchar(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.name)
    if not existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    cur.execute("SELECT * FROM characters WHERE uid=? AND name=?", (ctx.author.id,char))
    r = cur.fetchone()
    embed = hikari.Embed(title=char, color=common.color())
    emstring = lambda i: f"{common.emoji['sparkle'] if r[i] not in common.statstandice else common.emoji[f'd{r[i]}']} d{r[i]}, {'+' if r[i+1] > 0 else ''}{r[i+1]} / {'+' if r[i+2] > 0 else ''}{r[i+2]}"
    embed.add_field(f"{common.emoji['smarts']} SMARTS", emstring(5))
    embed.add_field(f"{common.emoji['charm']} CHARM", emstring(8))
    embed.add_field(f"{common.emoji['grit']} GRIT", emstring(11))
    embed.add_field(f"{common.emoji['vigor']} VIGOR", emstring(14))
    embed.add_field(f"{common.emoji['tussle']} TUSSLE", emstring(17))
    embed.add_field(f"{common.emoji['flight']} FLIGHT", emstring(20))
    embed.add_field("ESSENCE", f"{common.emoji['sparkle']} {r[2]}")
    embed.add_field("LAST ROLL", f"{r[4]} on {common.emoji[r[3] if r[3].lower() in common.statcats else 'sparkle']} {r[3]}")
    embed.set_footer("Ordered by: " + str(ctx.author))
    await ctx.respond(embed)

