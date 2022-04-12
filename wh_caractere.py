import json
import time
from urllib import request
from urllib.error import HTTPError
from datetime import datetime

WEBHOOK_URL =""
#général

headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

today=datetime.today()
g=0
print(today)

declencheur=datetime(today.year,today.month,23,22)
print('date déclencheur: {}'.format(declencheur))
print('yo')
fait=0
print(fait)
caractere2=186806
while g!=1:
    today=datetime.today()
    today1=today.isoformat(timespec='minutes')
    declencheur2=declencheur.isoformat(timespec='minutes')

    if declencheur2==today1:
        print('c\'est le jour')
        declencheur=declencheur.replace(day=today.day+1)
        if fait==1:
            fait=0
            fichier = open("caractere.txt", "r")
            caractere2 = fichier.read()
            caractere=caractere2
        else:
            fichier = open("caractere.txt", "r")
            caractere1 = fichier.read()
            caractere=int(caractere1)-caractere2
            caractere2=caractere1
        payload = {
            'embeds': [
                {
                    'title': 'Nombre de caractère du jour:',  # Le titre de la carte
                    'description': 'Aujourd\'hui nous avons envoyé __{}__ caractères.'.format(caractere),
                },
            ]
        }
        req = request.Request(url=WEBHOOK_URL,
                              data=json.dumps(payload).encode('utf-8'),
                              headers=headers,
                              method='POST')
        try:
            response = request.urlopen(req)
            print(response.status)
            print(response.reason)
            print(response.headers)
        except HTTPError as e:
            print('ERROR')
            print(e.reason)
            print(e.hdrs)
        print('date déclencheur quand pris: {}'.format(declencheur))

    temps_restant=abs(declencheur-today)
    print('temps restants:{}'.format(temps_restant))
    if today.hour >=21 and today.hour<23:
        print('passe')
        time.sleep(60)
    else:
        print('pas')
        time.sleep(1800)
