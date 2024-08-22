import lightbulb
import hikari
import common
import sqlite3
import random

plugin = lightbulb.Plugin('play', 'I used to rollll~ the dice')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

con = sqlite3.connect("./db/char.db")
cur = con.cursor()

def sil(lst):
    return [str(i) for i in lst]

@plugin.command
@lightbulb.option("amount", "Amount to boost", type=int)
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("boost", "Use essence to boost", aliases=["BOOST"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def boost(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return

    if ctx.options.amount < 0:
        await ctx.respond("Boost must be positive!")
        return
    
    query = f"SELECT essence, lastroll, lastrollstat FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    essence, lr, lrs, = cur.fetchone()

    if essence < ctx.options.amount:
        await ctx.respond("Not enough essence!")
        return
    
    essence -= ctx.options.amount
    lr += ctx.options.amount

    cur.execute("UPDATE characters SET essence=?, lastroll=? WHERE uid=? AND name=?", (essence, lr, ctx.author.id, char))
    con.commit()

    await ctx.respond(f"{char.capitalize()}'s {common.emoji[lrs]} {lrs.upper()} roll is actually {lr}!")

@plugin.command
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("fail", "Fail a check!", aliases=["FAIL"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def fail(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    
    query = f"SELECT essence FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    essence, = cur.fetchone()
    cur.execute("UPDATE characters SET essence=? WHERE uid=? AND name=?", (essence+1, ctx.author.id, char))
    con.commit()
    await ctx.respond("Better luck next time!\n" + f"Your essence has been updated to *{essence+1}*")

@plugin.command
@lightbulb.option("kwargs", "Extra keywords, for example 'magic'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, default="")
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("smarts", "Roll a SMARTS check", aliases=["SMARTS", "smart", "SMART", "intelligence", "INTELLIGENCE", "int", "INT"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def smarts(ctx: lightbulb.Context):
    common.log_com(ctx)
    kwargs = "" if ctx.options.kwargs == None else ctx.options.kwargs.lower().split(" ")
    stat="smarts"
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    query = f"SELECT {stat}_dice, {stat}_bonus, {stat}_magic FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    dice, bonus, magic = cur.fetchone()

    rolls = [random.randint(1, dice)]
    while rolls[-1] == dice:
        rolls.append(random.randint(1, dice))
    msg = f"{char.capitalize()} rolled {'**!** + '.join(sil(rolls))} + {bonus}"
    total = sum(rolls) +bonus
    
    if "magic" in kwargs:
        magicrolls = [random.randint(1, 4)]
        while magicrolls[-1] == 4:
            magicrolls.append(random.randint(1, dice))
        total += sum(magicrolls) + magic
        msg += f" + {'**!** + '.join(sil(magicrolls))} + {magic}"

    msg += f" for a total of {total} {common.emoji[stat]}"
    
    cur.execute("UPDATE characters SET lastrollstat=?, lastroll=? WHERE uid=? AND name=?", (stat, total, ctx.author.id, char))
    con.commit()
    
    await common.send_msg(ctx, msg)

@plugin.command
@lightbulb.option("kwargs", "Extra keywords, for example 'magic'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, default="")
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("charm", "Roll a CHARM check", aliases=["CHARM", "charisma", "CHARISMA", "cha", "CHA", "rizz", "RIZZ"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def charm(ctx: lightbulb.Context):
    common.log_com(ctx)
    kwargs = "" if ctx.options.kwargs == None else ctx.options.kwargs.lower().split(" ")
    stat="charm"
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    query = f"SELECT {stat}_dice, {stat}_bonus, {stat}_magic FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    dice, bonus, magic = cur.fetchone()

    rolls = [random.randint(1, dice)]
    while rolls[-1] == dice:
        rolls.append(random.randint(1, dice))
    msg = f"{char.capitalize()} rolled {'**!** + '.join(sil(rolls))} + {bonus}"
    total = sum(rolls) +bonus
    
    if "magic" in kwargs:
        magicrolls = [random.randint(1, 4)]
        while magicrolls[-1] == 4:
            magicrolls.append(random.randint(1, dice))
        total += sum(magicrolls) + magic
        msg += f" + {'**!** + '.join(sil(magicrolls))} + {magic}"

    msg += f" for a total of {total} {common.emoji[stat]}"
    
    cur.execute("UPDATE characters SET lastrollstat=?, lastroll=? WHERE uid=? AND name=?", (stat, total, ctx.author.id, char))
    con.commit()
    
    await common.send_msg(ctx, msg)

@plugin.command
@lightbulb.option("kwargs", "Extra keywords, for example 'magic'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, default="")
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("grit", "Roll a GRIT check", aliases=["GRIT"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def smarts(ctx: lightbulb.Context):
    common.log_com(ctx)
    kwargs = "" if ctx.options.kwargs == None else ctx.options.kwargs.lower().split(" ")
    stat="grit"
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    query = f"SELECT {stat}_dice, {stat}_bonus, {stat}_magic FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    dice, bonus, magic = cur.fetchone()

    rolls = [random.randint(1, dice)]
    while rolls[-1] == dice:
        rolls.append(random.randint(1, dice))
    msg = f"{char.capitalize()} rolled {'**!** + '.join(sil(rolls))} + {bonus}"
    total = sum(rolls) +bonus
    
    if "magic" in kwargs:
        magicrolls = [random.randint(1, 4)]
        while magicrolls[-1] == 4:
            magicrolls.append(random.randint(1, dice))
        total += sum(magicrolls) + magic
        msg += f" + {'**!** + '.join(sil(magicrolls))} + {magic}"

    msg += f" for a total of {total} {common.emoji[stat]}"
    
    cur.execute("UPDATE characters SET lastrollstat=?, lastroll=? WHERE uid=? AND name=?", (stat, total, ctx.author.id, char))
    con.commit()
    
    await common.send_msg(ctx, msg)

@plugin.command
@lightbulb.option("kwargs", "Extra keywords, for example 'magic'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, default="")
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("vigor", "Roll a VIGOR check", aliases=["VIGOR"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def vigor(ctx: lightbulb.Context):
    common.log_com(ctx)
    kwargs = "" if ctx.options.kwargs == None else ctx.options.kwargs.lower().split(" ")
    stat="vigor"
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    query = f"SELECT {stat}_dice, {stat}_bonus, {stat}_magic FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    dice, bonus, magic = cur.fetchone()

    rolls = [random.randint(1, dice)]
    while rolls[-1] == dice:
        rolls.append(random.randint(1, dice))
    msg = f"{char.capitalize()} rolled {'**!** + '.join(sil(rolls))} + {bonus}"
    total = sum(rolls) +bonus
    
    if "magic" in kwargs:
        magicrolls = [random.randint(1, 4)]
        while magicrolls[-1] == 4:
            magicrolls.append(random.randint(1, dice))
        total += sum(magicrolls) + magic
        msg += f" + {'**!** + '.join(sil(magicrolls))} + {magic}"

    msg += f" for a total of {total} {common.emoji[stat]}"
    
    cur.execute("UPDATE characters SET lastrollstat=?, lastroll=? WHERE uid=? AND name=?", (stat, total, ctx.author.id, char))
    con.commit()
    
    await common.send_msg(ctx, msg)

@plugin.command
@lightbulb.option("kwargs", "Extra keywords, for example 'magic'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, default="")
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("tussle", "Roll a smart check", aliases=["TUSSLE"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def tussle(ctx: lightbulb.Context):
    common.log_com(ctx)
    kwargs = "" if ctx.options.kwargs == None else ctx.options.kwargs.lower().split(" ")
    stat="tussle"
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    query = f"SELECT {stat}_dice, {stat}_bonus, {stat}_magic FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    dice, bonus, magic = cur.fetchone()

    rolls = [random.randint(1, dice)]
    while rolls[-1] == dice:
        rolls.append(random.randint(1, dice))
    msg = f"{char.capitalize()} rolled {'**!** + '.join(sil(rolls))} + {bonus}"
    total = sum(rolls) +bonus
    
    if "magic" in kwargs:
        magicrolls = [random.randint(1, 4)]
        while magicrolls[-1] == 4:
            magicrolls.append(random.randint(1, dice))
        total += sum(magicrolls) + magic
        msg += f" + {'**!** + '.join(sil(magicrolls))} + {magic}"

    msg += f" for a total of {total} {common.emoji[stat]}"
    
    cur.execute("UPDATE characters SET lastrollstat=?, lastroll=? WHERE uid=? AND name=?", (stat, total, ctx.author.id, char))
    con.commit()
    
    await common.send_msg(ctx, msg)

@plugin.command
@lightbulb.option("kwargs", "Extra keywords, for example 'magic'", modifier=lightbulb.OptionModifier.CONSUME_REST, required=False, default="")
@lightbulb.option("name", "The name of the character", type=str)
@lightbulb.command("flight", "Roll a FLIGHT check", aliases=["FLIGHT"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def flight(ctx: lightbulb.Context):
    common.log_com(ctx)
    kwargs = "" if ctx.options.kwargs == None else ctx.options.kwargs.lower().split(" ")
    stat="flight"
    char = common.clean_name(ctx.options.name)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    query = f"SELECT {stat}_dice, {stat}_bonus, {stat}_magic FROM characters WHERE uid=? AND name=?"
    cur.execute(query, (ctx.author.id, char))
    dice, bonus, magic = cur.fetchone()

    rolls = [random.randint(1, dice)]
    while rolls[-1] == dice:
        rolls.append(random.randint(1, dice))
    msg = f"{char.capitalize()} rolled {'**!** + '.join(sil(rolls))} + {bonus}"
    total = sum(rolls) +bonus
    
    if "magic" in kwargs:
        magicrolls = [random.randint(1, 4)]
        while magicrolls[-1] == 4:
            magicrolls.append(random.randint(1, dice))
        total += sum(magicrolls) + magic
        msg += f" + {'**!** + '.join(sil(magicrolls))} + {magic}"

    msg += f" for a total of {total} {common.emoji[stat]}"
    
    cur.execute("UPDATE characters SET lastrollstat=?, lastroll=? WHERE uid=? AND name=?", (stat, total, ctx.author.id, char))
    con.commit()
    
    await common.send_msg(ctx, msg)


