import random
from ast import alias
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

def abi():
    return("""```Boti käsklused on:
    !?"käsk"   - Kirjutades nii, saadan ma sõnumi dm-i.
    !tuleta    - Käsk tuleb kirjutada nii: !tuleta_ aasta-kuu-päev tund:minut_ sõnum
    !Korda_ n  - Kordab mida kasutaja ütles(n).
    !Täring_ n - Saab veeretada n arvu täringuid.
    !Tere      - Tervitab sind.
    !KPK_ n    - Bot mängib sinuga kivi-paber-kääre, n on sinu valik.
    ```""")
def kpk(valik):
    kivipaberkäärid = ["kivi", "paber","käärid"]
    arvuti_käivitus = random.choice(kivipaberkäärid)
    if arvuti_käivitus == "kivi":
        emoji = ":rock:"
    elif arvuti_käivitus == "paber":
        emoji = ":roll_of_paper:" 
    elif arvuti_käivitus == "käärid":
        emoji = ":scissors:"
    if arvuti_käivitus == valik:
        return(f"Viik! Bot valis: {arvuti_käivitus}  {emoji * 3}")
    elif (arvuti_käivitus == "kivi" and valik == "käärid") or (arvuti_käivitus == "paber" and valik == "kivi"):
        return(f"Bot võitis. Bot valis: {arvuti_käivitus}  {emoji * 3}")
    elif (arvuti_käivitus == "kivi" and valik == "paber") or (arvuti_käivitus == "käärid" and valik == "kivi"):
        return(f"Sina võitsid. Bot valis: {arvuti_käivitus}  {emoji * 3}")
    
def vastamine(sõnum: str) -> str:
    alam = sõnum.lower()    #Teeb sõnumi väikesteks tähtedeks, et süsteem lollikindlam oleks
    sõnum_eraldi = sõnum.strip().split("_ ")
    if alam[0] == "!":
        if alam[0:2] == "!?":   #Sõltuvalt kas sõnul läheb PMi või serverisse, eemaldab eest "!" või "!?"
            alam = alam[2:].strip().split("_ ")
        else:
            alam = alam[1:].strip().split("_ ")
        if alam[0] == "korda":
            return(str(sõnum_eraldi[1]))
        if alam[0] == "tere":
            return("Tere ka sulle!")
        if alam[0] == "täring":
            alam.append(1)
            vise = random.randint(int(alam[1]), int(alam[1])*6)
            return(f"Viskasite {alam[1]}. :game_die: ja saite {vise}")
        if alam[0] == "kpk":
            return(kpk(alam[1]))
        if alam[0] == "abi":
            return(abi())
        else:
            return("Ma ei saanud su käsklusest aru, proovi kirjutada `!abi`")
        

    