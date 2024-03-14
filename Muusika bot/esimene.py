
import discord
from discord.ext import commands




from teine import music_cog

client = commands.Bot(command_prefix='/')



client.add_cog(music_cog(client))

#kasutab antud tokenit boti jaoks
client.run("MTAzOTU3ODAxMTc4NTI1MjkyNQ.GsF7Gw.EL22Fg-oEki4gqKuPsiy3Tu1AKDIfovlpYIllM")