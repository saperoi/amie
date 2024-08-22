import lightbulb
import hikari
import common
import sqlite3

plugin = lightbulb.Plugin('stat', 'Statistics!!')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

con = sqlite3.connect("./db/char.db")
cur = con.cursor()

def listisnum(stats, naturalExclusingZeroAndOne):
    try:
        stats = [int(i) for i in stats]
    except:
        print(stats)
        return False
    if naturalExclusingZeroAndOne and min(stats) <= 1:
        print("hi")
        return False
    return True

async def await_answer(ctx, msg):
    await common.send_msg(ctx, msg)
    event = await ctx.app.event_manager.wait_for(hikari.GuildMessageCreateEvent, predicate=lambda e: e.message.author == ctx.author, timeout=30)
    try:
        answer = await ctx.app.rest.fetch_message(event.message.channel_id, event.message.id)
        answer = answer.content
    except:
        await ctx.respond("Didn't recieve response in time")
        raise Exception
    return answer

@plugin.command
@lightbulb.command("set", "Command group for setting stats", aliases=["SET", "SETSTATS", "SETSTAT", "setstat", "setstats"])
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommand)
async def setseries(ctx: lightbulb.Context):
    common.log_com(ctx)
    m = """
This command has several sub-commands
===
cast!set dice <char> S C G V T F
cast!set bonus <char> S C G V T F
cast!set magic <char> S C G V T F
===
These set the smart-, charm-, grit-, vigor-, tussle- and flight- stats for each category.
For Bonus and the Magic bonus, these may be any integer.
For Dice, they SHOULD uniquely be 4, 6, 8, 10, 12 and 20, but can technically also be any integer, this is advised to keep positive.
===
You can also set each stat individually like so:
cast!set stat <stat> <char> <category> X
or
cast!set stat <stat> <char> all <dice> <bonus> <magic>
"""
    await common.send_msg(ctx, m)

@setseries.child
@lightbulb.option("stat", "Stats, space delimited. 4, 6, 8, 10, 12 and 20 recommended", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("char", "Character", required=True)
@lightbulb.command("dice", "Sets the dice stats for a character", aliases=["DICE"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def dice(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.char)
    stats = ctx.options.stat.split(" ")
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    if len(stats) != 6:
        await ctx.respond("Inappropriate amount of numbers provided. Double-check your inputs. The numbers must be seperated by spaces")
        return
    if not listisnum(stats, True):
        await ctx.respond("Non-natural number less than 2 provided. Double-check your inputs.")
        return
    stats = [int(_) for _ in stats]

    msg = "Do you wish to give your character the following stats? Reply with 'yes' if this is what you want.\n"
    if len(set(stats)) != 6:
        msg+="Stats contain at least one duplicate die.\n"
    if False in [_ in common.statstandice for _ in stats]:
        msg+="Stats contain at least one die with a non-standard amount of sides.\n"
    msg += "\n".join([f"{common.statcats[i].upper()} d{stats[i]}" for i in range(6)])
    answer = await await_answer(ctx, msg)
    if 'yes' not in answer.lower():
        await ctx.respond("Operation cancelled.")
        return
    query = f"UPDATE characters SET {', '.join([_ + '_dice=?' for _ in common.statcats])} WHERE uid=? AND name=?"
    qtup = tuple(stats + [ctx.author.id, char])
    cur.execute(query, qtup)
    con.commit()
    await ctx.respond(f"Successfully set `{char}`'s dice stats to {stats}")

@setseries.child
@lightbulb.option("stat", "Stats, space delimited.", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("char", "Character", required=True)
@lightbulb.command("bonus", "Sets the bonus stats for a character", aliases=["BONUS"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def bonus(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.char)
    stats = ctx.options.stat.split(" ")
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    if len(stats) != 6:
        await ctx.respond("Inappropriate amount of numbers provided. Double-check your inputs. The numbers must be seperated by spaces")
        return
    if not listisnum(stats, False):
        await ctx.respond("Non-integer provided")
        return
    stats = [int(_) for _ in stats]
    
    query = f"UPDATE characters SET {', '.join([_ + '_bonus=?' for _ in common.statcats])} WHERE uid=? AND name=?"
    qtup = tuple(stats + [ctx.author.id, char])
    cur.execute(query, qtup)
    con.commit()
    await ctx.respond(f"Successfully set `{char}`'s bonus stats to {stats}")

@setseries.child
@lightbulb.option("stat", "Stats, space delimited.", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("char", "Character", required=True)
@lightbulb.command("magic", "Sets the bonus stats for a character", aliases=["MAGIC", "magicbonus", "MAGICBONUS"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def magicbonus(ctx: lightbulb.Context):
    common.log_com(ctx)
    char = common.clean_name(ctx.options.char)
    stats = ctx.options.stat.split(" ")
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return
    if len(stats) != 6:
        await ctx.respond("Inappropriate amount of numbers provided. Double-check your inputs. The numbers must be seperated by spaces")
        return
    if not listisnum(stats, False):
        await ctx.respond("Non-integer provided")
        return
    stats = [int(_) for _ in stats]
    
    query = f"UPDATE characters SET {', '.join([_ + '_magic=?' for _ in common.statcats])} WHERE uid=? AND name=?"
    qtup = tuple(stats + [ctx.author.id, char])
    cur.execute(query, qtup)
    con.commit()
    await ctx.respond(f"Successfully set `{char}`'s magic bonus stats to {stats}")

@setseries.child
@lightbulb.option("cont", "Either in format (category) X, or all (dice) (bonus) (magic)", modifier=lightbulb.OptionModifier.CONSUME_REST, required=True)
@lightbulb.option("char", "Character", required=True)
@lightbulb.option("stat", "Stat to change", choices=common.statcats, required=True)
@lightbulb.command("stat", "Sets the bonus stats for a character", aliases=["STAT"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def setstat(ctx: lightbulb.Context):
    common.log_com(ctx)

    char = common.clean_name(ctx.options.char)
    if not common.existcharcheck(ctx.author.id, char):
        await ctx.respond(f"Character `{char}` doesn't exist")
        return

    stat = ctx.options.stat.lower()
    if stat not in common.statcats:
        await ctx.respond(f"`{stat}` is not a valid stat to change")
        return
    
    cont = str(ctx.options.cont).split(" ")
    cat = cont[0].lower()
    if cat not in ["dice", "magic", "bonus", "all"]:
        await ctx.respond(f"`{cat}` is not a valid stat category")
        return
    
    cont = cont[1:]
    if (len(cont) != 3 and cat=="all") or (len(cont) != 1 and cat!="all"):
        await ctx.respond("Inappropriate amount of numbers provided. Double-check your inputs. The numbers must be seperated by spaces")
        return

    if not listisnum([cont[1:] if cat=="all" else cont][0], False):
        await ctx.respond("Non-integer provided")
        return
    if not listisnum([cont if cat=="dice" else [cont[0]] if cat=="all" else ['2']][0], True):
        await ctx.respond("Non-natural number less than 2 provided. Double-check your inputs.")
        return

    msg = ""
    if cat in ["dice", "all"]:
        query = f"UPDATE characters SET {stat}_dice=? WHERE uid=? AND name=?"
        cur.execute(query, (cont[0], ctx.author.id, char))
        msg += f"Successfully set `{char}`'s {stat} dice to {cont[0]}" + "\n"
        cont = cont[1:]

    if cat in ["bonus", "all"]:
        query = f"UPDATE characters SET {stat}_bonus=? WHERE uid=? AND name=?"
        cur.execute(query, (cont[0], ctx.author.id, char))
        msg += f"Successfully set `{char}`'s {stat} bonus to {cont[0]}" + "\n"
        cont = cont[1:]

    if cat in ["magic", "all"]:
        query = f"UPDATE characters SET {stat}_magic=? WHERE uid=? AND name=?"
        cur.execute(query, (cont[0], ctx.author.id, char))
        msg += f"Successfully set `{char}`'s {stat} magic bonus to {cont[0]}" + "\n"
        cont = cont[1:]
    con.commit()
    await ctx.respond(msg)
