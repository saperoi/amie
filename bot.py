import common
import hikari
import lightbulb
from lightbulb.ext import tasks
import random
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")
uid = os.getenv("UID")

activities = [
    hikari.Activity(name="the " + prefix + "help command", type=hikari.ActivityType.WATCHING),
    hikari.Activity(name="with my grimoire", type=hikari.ActivityType.PLAYING)
]

bot = lightbulb.BotApp(token=token, prefix=[prefix, prefix.replace("/", "\/"), "<@" + uid + "> "], intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT)

tasks.load(bot)

@tasks.task(s=45, auto_start=True, pass_app=True)
async def bot_status(bot):
    await bot.update_presence(activity=random.choice(activities), status=hikari.presences.Status.ONLINE)

bot.load_extensions_from("./cogs")
bot.run(activity=random.choice(activities), status=hikari.presences.Status.ONLINE)