from random import choice
import os

donne =    ["prenom1","prenom2","prenom3","prenom4","prenom5","prenom6"]

recois = donne[:]
liste = [ [ None for y in range( 2 ) ] for x in range(0,len(donne) ) ]

def picksomeone(recois) :
    for i in range(0, len(donne)):
        donne_name = donne[i]
        recois_name = choice(recois)
        liste[i][0] = donne_name
        liste[i][1] = recois_name
        recois.remove(recois_name)
    for i in range(0, len(liste)) :
        if liste[i][0] == liste[i][1] :
            print("Found same ... Reroll !")
            recois = donne[:]
            picksomeone(recois)

picksomeone(recois)

""" -> Pour te faire spoil ... et vérifier que cela fontionne correctement !
for i in  range(0, len(liste)):
    print (liste[i][0] + " --> " + liste[i][1])
"""

if not os.path.exists('people/'):
    os.makedirs('people/')

with open('people/_message.txt','w',encoding='utf-8-sig') as m:
    for i in  range(0, len(liste)):
        with open(('people/' + liste[i][0] + '.txt'),'w',encoding='utf-8-sig') as f :
                f.write(liste[i][0] + " --> " + liste[i][1])
                m.write("Salut "+liste[i][0]+" Comment ça va ? 😏\nLets go pour le papa noel random ! 🎅\nRegarde le fichier pour savoir à qui tu fais un cadeau ✨🎁\nOublie pas max 10€ !😱\nBisous💖\n\n")
        f.close()
m.close()

print("Done :)\n-> check out the files in the people folder !")
