import sqlite3

emoji = {
    "d20": "<:d20:1266429492415696916>",
    "d12": "<:d12:1266429491656528015>",
    "d10": "<:d10:1266429490716868679>",
    "d8": "<:d8:1266429489999773928>",
    "d6": "<:d6:1266429488908996693>",
    "d4": "<:d4:1266429487940108289>",
    "smarts": "<:smarts:1266429499189362740>",
    "charm": "<:charm:1266429553052618814>",
    "grit": "<:grit:1266429580659658802>",
    "vigor": "<:vigor:1266429568797900892>",
    "tussle": "<:tussle:1266429496219668510>",
    "flight": "<:flight:1266429493451554856>",
    "sparkle": "<:sparkle:1266436941386088468>",
    "empty": "<:empty:1266448012528324638>"
}
statcats = ['smarts', 'charm', 'grit', 'vigor', 'tussle', 'flight']
statstandice = [4, 6, 8, 10, 12, 20]

con = sqlite3.connect("./db/char.db")
cur = con.cursor()
def existcharcheck(user, char):
    cur.execute("SELECT COUNT(*) FROM characters WHERE uid=? AND name=?", (user, char))
    r = bool(cur.fetchone()[0])
    con.commit()
    return r