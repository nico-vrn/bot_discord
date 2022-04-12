import boto3
import discord
import json
import re
import sys
import time
import asyncio

print('version:', sys.version)

s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
client2 = boto3.client('comprehend')

client=discord.Client()

@client.event
async def on_ready():
    global a
    print('Logged in {} as {}'.format(client.user.name, client.user.id))
    print('------')
    await client.change_presence(activity=discord.Game(name='Tester tes sentiments'))

black_channel=[695247694427324468, 694926082763259954,\
696300529030135878, \
718471558024134656, 723229780979482630, 718471652198842469,
718471236182736936] #sapm, bot, test bot, coloc, 4 stat seig
caractere_non=["http","https", "```", 'https://']

listemj=[u'\U0001F44D', u'\U0001F44E', u'\U0001F610', u'\U0001F928']

# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

async def del_reaction():
    await asyncio.sleep(10)
    await message.clear_reaction(emojii)

@client.event
async def on_message(message):
    #channelused =client.get_channel(698139746853060649) #test
    #channelused =client.get_channel(694926082763259954) #bot
    channelused=message.channel
    channeltest =client.get_channel(698139746853060649) #test

    if message.author.bot or message.author==client.user or message.content in caractere_non or message.channel.id in black_channel:
        print('channel ou caractère non pris en compte')
        return
    text=message.content
    print(message.content)

    queue = client2.batch_detect_sentiment(
        TextList=[
            text
        ],
        LanguageCode='fr'
    )

    test=queue['ResultList']
    resultatlist=test[0]
    sentiment=resultatlist['Sentiment']
    sentimentscore=resultatlist['SentimentScore']
    positif=sentimentscore['Positive']
    negatif=sentimentscore['Negative']
    neutre=sentimentscore['Neutral']

    # You can now access identifiers and attributes
    print("coucou")
    print(message.content)
    print('positif:',positif)
    print('negatif:', negatif)
    print('neutre:', neutre)
    #print(resultatlist)
    #await channeltest.send("**message**: {}, **de**: {}, **sentiment**: {}"
    #.format(message.content, message.author.id, sentiment))

    if sentiment=='POSITIVE':
        emojii=listemj[0]
    elif sentiment=='NEGATIVE':
        emojii=listemj[1]
    elif sentiment=='NEUTRAL':
        emojii=listemj[2]
    elif sentiment=='MIXED':
        emojii=listemj[3]



    await message.add_reaction(emojii)
    print(emojii)
    """del_reaction()"""
    #time.sleep(10)
    await message.clear_reaction(emojii)

    def valeur():
        global maxx
        global total
        global sortie_neutre
        global sortie_negatif
        global sortie_positif
        sortie_positif=sortie2[i][0]['Positive']
        sortie_negatif=sortie2[i][0]['Negative']
        sortie_neutre=sortie2[i][0]['Neutral']
        def find_key(v):
            for k, val in sortie2[i][0].items():
                if v == val:
                    return k
        if max(sortie_positif,sortie_negatif,sortie_neutre)==sortie_positif:
            maxx=find_key(sortie_positif)
        elif max(sortie_positif,sortie_negatif,sortie_neutre)==sortie_negatif:
            maxx=find_key(sortie_negatif)
        elif max(sortie_positif,sortie_negatif,sortie_neutre)==sortie_neutre:
            maxx=find_key(sortie_neutre)
        total=sortie_positif+sortie_negatif+sortie_neutre
        print("total:{}".format(total))
        sortie_positif=(sortie_positif/total)*100
        print("pos:{}".format(sortie_positif))
        sortie_negatif=(sortie_negatif/total)*100
        print("neg:{}".format(sortie_negatif))
        sortie_neutre=(sortie_neutre/total)*100
        print("neutr:{}".format(sortie_neutre))

    s={'ID':{message.author.id:[sentimentscore]}}

    with open('data.json') as json_data:
        data_dict = json.load(json_data)
        data_dict2=data_dict['ID']
        """print(data_dict2)"""
        if str(message.author.id) in list(data_dict2.keys()):
            print('bon')
            id=str(message.author.id)
            positif2=data_dict2[id][0]['Positive']
            negatif2=data_dict2[id][0]['Negative']
            neutre2=data_dict2[id][0]['Neutral']
            """print('pst 2:',positif2)
            print('ngt 2:',negatif2)
            print('neut 2:',neutre2)"""
            positif2=positif+positif2
            negatif2=negatif+negatif2
            neutre2=neutre+neutre2
            """print('pst2 prs:',positif2)
            print('ngt2 prs:',negatif2)
            print('neut2 prs:',neutre2)"""
            data_dict2[id][0]['Positive']=positif2
            data_dict2[id][0]['Negative']=negatif2
            data_dict2[id][0]['Neutral']=neutre2
            with open("data.json","w+") as write1_file:
                json.dump(data_dict,write1_file)
            """print(data_dict)"""
        else:
            serial=data_dict['ID'][message.author.id]=[sentimentscore]
            with open("data.json", "w+") as write_file:
                json.dump(data_dict,write_file)
            print(data_dict)

    if message.content.startswith('$sentiment') and message.author!=client.user:
        msg=message.content.split()
        #msg=msg[1]
        t=2
        with open("data.json") as lire_data:
            sortie1 = json.load(lire_data)
            sortie2 = sortie1['ID']
            list_clé=list(sortie2.keys())
        if t==3:
            for i in list_clé:
                print(i)
                """print(round(sortie_positif), '% pos')
                print(round(sortie_negatif), '% neg')
                print(round(sortie_neutre), '% neut')"""
                valeur()
                await channelused.send('<@{}> à pour score: {} % \
en positif, {} % en négatif, {} % en neutre ce qui fait \
une prédominance de **{}**'.format(i,round(sortie_positif), \
round(sortie_negatif),round(sortie_neutre), maxx))
        else:
            i=message.mentions
            i=str(i[0].id)
            print(i)
            valeur()
            await channelused.send('<@{}> à pour score: {} % \
en positif, {} % en négatif, {} % en neutre ce qui fait \
une prédominance de **{}**'.format(i,round(sortie_positif), \
round(sortie_negatif),round(sortie_neutre), maxx))


    msg=message.content.split()
    print(msg)
    for i in range(len(msg)):
        print(msg)
        print(i)
        if msg[i]=='<@!720396368564453516>':
            print("la")
            await message.edit.content('test')
            await channelused.send('<@{}> il faut pas me mentionner'.format(message.author.id))
        else :
            print("ici")

client.run("")
