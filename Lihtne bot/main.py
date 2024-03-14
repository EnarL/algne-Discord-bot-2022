import discord, vasted, asyncio, datetime
from discord.ext import commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def saada_sõnum(sõnum, kasutaja_sõnum, privaatne): #Saadab sõnumi pärast seda kui on kasutajalt käsu saanud
    try:
        vastus = vasted.vastamine(kasutaja_sõnum)
        if privaatne == True:
            await sõnum.author.send(vastus)
        else:
            await sõnum.channel.send(vastus)
    except:
        print("Jooksin kokku")

async def tuleta(sõnum, kasutaja_sõnum, kasutaja):
    try:
        sõnum_eraldi = kasutaja_sõnum.strip().split("_ ")
        praegu = datetime.datetime.now()
        siis = datetime.datetime.strptime(sõnum_eraldi[1], "%Y-%m-%d %H:%M")
        ooteaeg = (siis-praegu).total_seconds()
        await asyncio.sleep(ooteaeg)
        if sõnum_eraldi[0] == "!tuleta":
            await sõnum.channel.send(f"<@{kasutaja}> !MEELDETULETUS!: {sõnum_eraldi[2]}")
        else:
            await sõnum.author.send(f"<@{kasutaja}> !MEELDETULETUS!: {sõnum_eraldi[2]}")
    except:
        await sõnum.channel.send("Proovige uuesti, midagi käskluses läks nihu.")



@bot.event
async def on_ready():
    print(f"Me oleme sisse logitud {bot.user} kasutajana")

@bot.event
async def on_message(sõnum): #Tuvastab kasutaja sõnumi
    if sõnum.author == bot.user:
        return
    kasutaja = str(sõnum.author)
    id = sõnum.author.id
    kasutaja_sõnum = str(sõnum.content)
    kanal = str(sõnum.channel)
    print(f"{kasutaja} ütles: '{kasutaja_sõnum}' ({kanal})")
    if kasutaja_sõnum[0:7] == "!tuleta" or kasutaja_sõnum[0:8] == "!?tuleta":
        await tuleta(sõnum, kasutaja_sõnum, id)
    elif kasutaja_sõnum[0:2] == "!?": #Tuvastab kas sõnum läheb PMi või serverisse
        await saada_sõnum(sõnum, kasutaja_sõnum, privaatne=True)
    else:
        await saada_sõnum(sõnum, kasutaja_sõnum, privaatne=False)

bot.run("MTAzOTUzMjU0OTkzODA5NDE1MQ.GhoxAq.duq-k9pUaOip_wQEZhj90yAO_Gg2nBzIshO1JU")