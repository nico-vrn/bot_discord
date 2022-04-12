import discord
from discord.ext import tasks, commands
import datetime
import time
from datetime import datetime

client=discord.Client()
today=datetime.now()

print(today)
fichier = open("caractere.txt", "r")
caractere = fichier.read()
caractere=int(caractere)
print(caractere)
white_channel=[718471236182736936,695247694427324468,\
694926082763259954,696300529030135878,698139746853060649,\
718471558024134656,718471652198842469,718474156680937515]

@client.event
async def on_ready():
    global a
    print('Logged in {} as {}'.format(client.user.name, client.user.id))
    print('------')

@client.event
async def on_message(message):
    global caractere
    if message.author.bot or message.author==client.user or message.channel.id in white_channel:
        print('channel interdit')
        return
    print(message.content)
    print(len(message.content))
    caractere+=len(message.content)
    if message.content=="!caractere" and message.author != client.user:
        caractere-=len(message.content)
        await message.channel.send('on en est a {} caracteres.'.format(caractere))
    print(caractere)
    fichier = open("caractere.txt", "w")
    fichier.write(str(caractere))



client.run("")
