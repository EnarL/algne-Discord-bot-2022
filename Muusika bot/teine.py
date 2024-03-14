
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       #Mängib või on pausil
        self.mängib = False
        self.pausil = False
        #[laul,kanal], optionid mis on vajalikud, et FFMPEG ja YDL töötaks sujuvalt
        self.muusika_järjekord = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

     #otsib laulu youtubest
    def otsi(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}


    def mängi_järgmisena(self):
        if len(self.muusika_järjekord) > 0:
            self.mängib = True
            #Saab esimese url-i
            url = self.muusika_järjekord[0][0]['source']
           #Eemaldab listist esimese elemendi, sest seda laulu juba parjasti esitatakse
            self.muusika_järjekord.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.mängi_järgmisena())
        else:
            self.mängib = False
    #ctx on context ja see peab eksisteerima iga funktsiooni juures kus tehakse mingi command
    #Lõpmatult kontrollib loopi
    async def mängi_muusikat(self, ctx):
        if len(self.muusika_järjekord) > 0:
            self.mängib = True
            url = self.muusika_järjekord[0][0]['source']
            #Ürita vciga ühenduda kui juba pole
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.muusika_järjekord[0][1].connect()
                #Kui ei õnnestunud vciga ühenduda
                if self.vc == None:
                    await ctx.send("Ei õnnestunud vciga ühenduda")
                    return
            else:
                await self.vc.move_to(self.muusika_järjekord[0][1])
            #Eemaldab listist esimese elemendi, sest seda laulu juba parjasti esitatakse
            self.muusika_järjekord.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.mängi_järgmisena())
        else:
            self.mängib = False
    @commands.command(name="mängi", aliases=["p","playing"], help="Mängib laulu youtubest")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #Sa pead olema ühendatud häälkanaliga et bot teaks kuhu liituda
            await ctx.send("Ühenda häälkanaliga")
        elif self.pausil:
            self.vc.resume()
        else:
            song = self.otsi(query)
            if type(song) == type(True):
                await ctx.send("Ei saanud laulu esitada, proovi midagi muud")
            else:
                await ctx.send("Laul lisati järjekorda")
                self.muusika_järjekord.append([song, voice_channel])
                
                if self.mängib == False:
                    await self.mängi_muusikat(ctx)

    @commands.command(name="paus", aliases = ["pausil"], help="Paneb parajasti kõlava laulu pausile")
    async def pause(self, ctx, *args):
        if self.mängib:
                self.mängib = False
                self.pausil = True
                self.vc.pause()
        elif self.pausil:
                self.pausil = False
                self.mängib = True
                self.vc.resume()
    @commands.command(name = "jätka", aliases=["j"], help="Jätkab poolelioleva laulu esitamist")
    async def resume(self, ctx, *args):
        if self.pausil:
            self.pausil = False
            self.mängib = True
            self.vc.resume()

    @commands.command(name="järgmine", aliases=["n"], help="Lõpetab praeguse laulu mängimise ja alustab järgmise laulu mängimisega")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #mängib järgmise laulu järjekorrast kui eksisteerib
            await self.mängi_muusikat(ctx)
            if self.mängib:
                self.mängib = False
                self.pausil = True
                self.vc.pause()
    @commands.command(name="järjekord", aliases=["q"], help="Kuvab järjekorras olevad laulud")
    async def järjekord(self, ctx):
        tagastus_väärtus = ""
        for i in range(0, len(self.muusika_järjekord)):
            # kuvab maksimaalselt 10 laulu, mis on parajasti järjekorras
            if (i > 10): break
            tagastus_väärtus += self.muusika_järjekord[i][0]['title'] + "\n"
        if tagastus_väärtus != "":
            await ctx.send(tagastus_väärtus)
        else:
            await ctx.send("Järjekorras pole muusikat")
    @commands.command(name="tühjenda", aliases=["c", "bin"], help="Peatab muusika ja tühjendab järjekorra")
    async def clear(self, ctx):
        if self.vc != None and self.mängib:
            self.vc.stop()
        self.muusika_järjekord = []
        await ctx.send("Tühjendati muusika järjekord")

    @commands.command(name="eemalda", aliases=["disconnect", "d"], help="Eemaldab boti Voice kanalist")
    async def dc(self, ctx):
        self.mängib = False
        self.pausil = False
        await self.vc.disconnect()
