import discord
import wikipedia
import datetime
import asyncio
import time
from datetime import datetime
from discord.ext import tasks, commands
from discord.utils import get
import sys
print("Version ",sys.version)

client = discord.Client()
wikipedia.set_lang('fr')
today=datetime.now()

@client.event
async def on_ready():
    global a
    print('Logged in {} as {}'.format(client.user.name, client.user.id))
    print('------')
    await client.change_presence(activity=discord.Game(name='rechercher sur wikipédia'))

dict={'liensin':'https://eu.bbcollab.com/guest/fc149112943547fcbc5190871949d453',\
 'lienett':'https://eu.bbcollab.com/guest/bd391fbc751048aebf7b31f1ab05b04f', \
 'lienphysique':'https://eu.bbcollab.com/guest/4670bc8e09164991b850f022a24de274', \
 'lienmath':'https://eu.bbcollab.com/guest/ba377a37d73f4363af9e0f43019b1ada', \
 'lienAC':'https://eu.bbcollab.com/collab/ui/session/guest/7814bb3a19f94a4d98acc291ecc850f3'}

nico='nico'
print('coucou {}, ca va?'.format(nico))
print('date aujourd\'hui: {}'.format(today))

@client.event
async def on_message(message):
    #channelused =client.get_channel(698139746853060649) #test
    #channelused =client.get_channel(694926082763259954) #bot
    channelused =message.channel

    if message.author.bot :
        return
    if message.content[0]=="%" and message.author != client.user:
        try:
            recherche=message.content[1:]
            print(recherche)
            cherche=wikipedia.page(recherche)
            await channelused.send(wikipedia.summary(recherche,sentences=3))
            await channelused.send(cherche.url)
        except:
            await channelused.send('Ce nom n\'existe pas, essaye en un autres')
            await asyncio.sleep

    if message.content[0]=='£' and message.author != client.user:
        channelrappel =client.get_channel(696300529030135878)
        msg=message.content.split()
        print(msg)
        pour=(' ').join(msg[:4])  #str(msg[1]+" "+str(msg[2])+" "+str(msg[3]))
        pour=pour.replace('£', '')
        matiere=msg[4]
        time1=msg[5]
        time2=msg[6]
        lien1=msg[7]
        lien=dict.get(lien1)
        await channelrappel.send('__{}:__ \n **-{}-{}, {}**: {}'.format(pour,time1,time2,matiere,lien))

    listemj=[client.get_emoji(722020385402650624),client.get_emoji(722021123759538227),
    client.get_emoji(722020322731098152),u'\U0001F921',u'\U0001F63C',u'\U0001F98A', u'\U0001F43A',
    u'\U0001F981', u'\U0001F42F']

    if message.author.id == "":
        print("Lucas envoi un message")
        i=0
        while i<9:
            emoji=listemj[i]
            await message.add_reaction(emoji)
            i+=1
    if message.author.id == "328545924777246721":
        print("spam Mathieu")
        i=0
        while i<50:
            await channelused.send("&spamlog")
            i+=1
client.run("Njk2Mjc5ODg2NjkxODI3NzUy.XombLQ.sflZR9gyvbfqJcs-P50guQC1jfY")
