import lightbulb
import hikari
from datetime import datetime
from dataclasses import dataclass
import textwrap
import random
import requests
import codecs
import base64
import os
import sqlite3

owner_id = [738772518441320460, 211560258311553025]
@lightbulb.Check
def owners_only(ctx: lightbulb.Context) -> bool:
    return ctx.author.id in owner_id

conmisc = sqlite3.connect("./db/misc.db")
curmisc = conmisc.cursor()

def cookies_table():
    curmisc.execute("CREATE TABLE IF NOT EXISTS misc_vars(key TEXT, value TEXT)")

    curmisc.execute("SELECT * FROM misc_vars WHERE key=?", ("cookies",) )
    if curmisc.fetchall() == []:
        curmisc.execute("INSERT INTO misc_vars VALUES (?, ?)", ("cookies", "0") )
    conmisc.commit()

    curmisc.execute("SELECT value FROM misc_vars WHERE key=?", ("cookies", ) )
    cookie_count, = curmisc.fetchone()
    cookie_count = str(int(cookie_count) +1)
    curmisc.execute("UPDATE misc_vars SET value=? WHERE key=?", (cookie_count, "cookies") )
    conmisc.commit()

def log_com(ctx: lightbulb.Context):
    cookies_table()
    commlog = codecs.open("log.txt", "a", "utf_16")
    ms = datetime.now().strftime("%D %H:%M:%S") + " : " + str(ctx.guild_id) + " : " + ctx.author.username + "#" + str(ctx.author.discriminator) +  " - " + str(ctx.author.id) + " : "
    try:
        ms += str(ctx.event.content)
    except:
        ms += f"{ctx.command.name} {ctx.raw_options}"
    commlog.write(ms + "\n")
    commlog.close()
    print(ms)

def user_id_check(u):
    if str(u).isnumeric():
        return int(u)
    elif type(u) == str:
        if u[0] == "<" and u[1] == "@" and u[-1] == ">":
            return int(u.replace('<', '').replace('>', '').replace('@', ''))
        else:
            raise ValueError
    else:
        raise ValueError

async def send_msg(ctx: lightbulb.Context, txt: str):
    lines = textwrap.wrap(txt, 2000, break_long_words=False, replace_whitespace=False)
    for j in range(len(lines)):
        await ctx.respond(lines[j])

# https://stackoverflow.com/questions/35772848/python-retrieve-a-file-from-url-and-generate-data-uri
def url2uri(url):
    response = requests.get(url)
    content_type = response.headers["content-type"]
    encoded_body = base64.b64encode(response.content)
    return "data:{};base64,{}".format(content_type, encoded_body.decode())

def color():
    return random.randint(0x0, 0xffffff)

def clean_name(name):
    return "".join([_ for _ in name if _.isalnum() or _.isspace()])
