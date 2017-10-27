from pip._vendor import requests
from xml.etree import ElementTree
from tkinter import *
import xmltodict
import re
import os
import sys

#Grootte van het programma en het aanmaken van de root variabele
root = Tk()
root.geometry("1400x1020")
root.resizable(0, 0)
root.configure(bg='#FFCC18')
errormessage = StringVar()

#Foto label met het logo van de NS
photo = PhotoImage(file='NS.png')
photolabel = Label(master=root, image=photo, bg='#FFCC18')
photolabel.pack(side=TOP, pady=2, padx=2)
#Welkomst tekst
welkom = Label(master=root, text='Welkom bij de NS', bg='#FFCC18', fg='#000066')
welkom.config(font=("Calibri", 44, 'bold'))
welkom.pack()

#Aangeven naar de gebruiker toe dat hij/zij de eerste letter van zijn/haar station moet kiezen
gebruikerkeuze = Label(master=root, text='Kies de eerste letter van uw station', height=1, bg='#FFCC18', fg='#000066')
gebruikerkeuze.config(font=("Calibri", 16))
gebruikerkeuze.pack()

#Errorlabel voor het weergeven van fouten
errorlabel = Label(master=root, textvariable=errormessage, justify="center", fg='#000066', bg='#FFCC18')
errorlabel.config(font=("Calibri", 14, 'bold'))
errorlabel.pack()

#Listbox voor het kiezen van de eerste letter
alfabetkeuzebox = Listbox(root, bg='#FFCC18', fg='#000066')
alfabetkeuzebox.config(font=("Calibri", 12, 'bold'))
alfabetkeuzebox.place(x=500, y=270)
#Listbox voor het kiezen van het station na aanklikken eerste letter
stationkeuzebox = Listbox(root, bg='#FFCC18', fg='#000066')
stationkeuzebox.config(font=("Calibri", 12, 'bold'))
stationkeuzebox.place(x=710, y=270)

#Vertrektijdlabel 
tijdlabel = Label(master=root, text='Vertrektijd', bg='#FFCC18', fg='#000066')
tijdlabel.config(font=("Calibri", 12, 'bold'))
tijdlabel.place(x=0, y=510)
#Eindbestemminglabel
eindbestemminglabel = Label(master=root, text='Eindbestemming', bg='#FFCC18', fg='#000066')
eindbestemminglabel.config(font=("Calibri", 12, 'bold'))
eindbestemminglabel.place(x=170, y=510)
#Treinsoortlabel
treinsoortlabel = Label(master=root, text='Trein soort', bg='#FFCC18', fg='#000066')
treinsoortlabel.config(font=("Calibri", 12, 'bold'))
treinsoortlabel.place(x=330, y=510)
#Aanbiederlabel
aanbiederlabel = Label(master=root, text='Aanbieder', bg='#FFCC18', fg='#000066')
aanbiederlabel.config(font=("Calibri", 12, 'bold'))
aanbiederlabel.place(x=490, y=510)
#Spoorlabel
spoorlabel = Label(master=root, text='Spoor', bg='#FFCC18', fg='#000066')
spoorlabel.config(font=("Calibri", 12, 'bold'))
spoorlabel.place(x=660, y=510)
#Tussenstoplabel
tussenstoplabel = Label(master=root, text='Tussenstop', bg='#FFCC18', fg='#000066')
tussenstoplabel.config(font=("Calibri", 12, 'bold'))
tussenstoplabel.place(x=820, y=510)
#Het hele alfabet wordt d.m.v een for loop in de alfabetkeuzebox gedaan. Daarna wordt een doubleclick event gebind op de box met een lambda expressie naar de volgende functie
def findstation():
    alfabet = map(chr, range(65, 91))
    for letter in alfabet:
      alfabetkeuzebox.insert(END, letter)
    alfabetkeuzebox.bind("<Double-Button-1>", lambda x: selected())

findstation()
#Korte omschrijving functie: de selected functie neemt de aangeklikte keuze van de gebruiker op en slaat die op in een variabele,
#Vervolgens een API call om alle stations op te halen, de stationnamen worden opgeslagen in een list
#De aangeklikte letter wordt vergeleken met de begin letter van elk station uit de list
def selected():
   #Aangeklikte keuze ophalen
   gekliktekeuze=str(alfabetkeuzebox.get(alfabetkeuzebox.curselection()))
   #Stationbox leeg maken voordat er nieuwe data in komt
   stationkeuzebox.delete(0, END)
   #Api call voor alle stations
   url = 'http://webservices.ns.nl/ns-api-stations-v2?_ga=2.130333579.543900054.1509023690-1596014411.1509023690'
   authentication=('manu-s1996@hotmail.com','1WbuU23CPkCeTcnjfAT7uow7hZYRLkmjap0IoRbUXl4dtZ06PLsiWA')
   response = requests.get(url, auth=authentication)
   #Als de status code niet 200 is dan is er een storing.
   if response.status_code != 200:
       errormessage.set("Er is een storing, probeert u het later nog eens")
   #XML parsen naar dictionary
   allstations = xmltodict.parse(response.text)
   #Lege list aanmaken
   stationsnamen = []
   #Door de dictionary heen itereren en alle stationsnamen opslaan in de list
   for station in allstations['Stations']['Station']:
        stationsnamen.append(station['Namen']['Kort'])
   #Over alle elementen in de list itereren, als naam (single element) begint met de gekozen letter dan wordt het station in de stationkeuzebox gedaan
   for naam in stationsnamen:
       if naam.startswith(gekliktekeuze):
            stationkeuzebox.insert(END, naam)
       #Doubleclick op een keuze uit de stationkeuzebox met een lambda expressie om de volgende functie aan te roepen
       stationkeuzebox.bind("<Double-Button-1>", lambda x: getvertrektijden())

#Korte omschrijving functie getvertrektijden:
#Stationkeuze wordt opgehaald, daarna wordt ere een API call gemaakt om de specifieke stations op te halen
def getvertrektijden():
    #Get stationkeuze
    stationkeuze=str(stationkeuzebox.get(stationkeuzebox.curselection()))
    #Api call
    url = 'http://webservices.ns.nl/ns-api-avt'
    #parameters worden in een payload variabele meegenomen
    payload = {'station' : stationkeuze }
    authentication=('manu-s1996@hotmail.com','1WbuU23CPkCeTcnjfAT7uow7hZYRLkmjap0IoRbUXl4dtZ06PLsiWA')
    response = requests.get(url,params=payload, auth=authentication)
    #Geen verbinding met de API = storing
    if response.status_code != 200:
        errormessage.set("Er is een storing, probeert u het later nog eens")
    #XML parsen naar dictionary
    vertrekXML = xmltodict.parse(response.text)
    beginstation(vertrekXML)

#Korte omschrijving functie beginstation:
#Eerst worden alle listboxes leeggemaakt, daarna wordt er over de dictionary heen geitereert en worden de listboxes voor het weergeven van de vertrekdata van treinen gevuld.
def beginstation(vertrekXML):
    #Listboxes leegmaken
    tussenstopbox.delete(0, END)
    vertrektijdbox.delete(0, END)
    eindbestemmingbox.delete(0, END)
    treinsoortbox.delete(0, END)
    vervoerderbox.delete(0, END)
    vertrekspoorbox.delete(0, END)
    #Loop voor itereren over dictionary
    for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
        try:
            vertrektijd = vertrek['VertrekTijd']
            vertrektijd = vertrektijd[11:16]
            eindbestemming = vertrek['EindBestemming']
            treinsoort = vertrek['TreinSoort']
            tussenstop = vertrek['RouteTekst']
            vervoerder = vertrek['Vervoerder']
            vertrekspoor = vertrek['VertrekSpoor']['#text']
            print(tussenstop)
            print(vertrektijd)
            tussenstopbox.insert(END, tussenstop)
            vertrektijdbox.insert(END, vertrektijd)
            eindbestemmingbox.insert(END, eindbestemming)
            treinsoortbox.insert(END, treinsoort)
            vervoerderbox.insert(END, vervoerder)
            vertrekspoorbox.insert(END, vertrekspoor)
        except KeyError:
            continue


def yview(*args):
        tussenstopbox.yview(*args)
        vertrektijdbox.yview(*args)
#scrollbar voor het gesynchroniseerd scrollen van alle listboxes
scrollbar = Scrollbar(orient='vertical')
scrollbar.config(command=yview)

#Functie voor het scrollen van de listboxes, elke listboxes wordt met elkaar vergeleken en als 1 listbox scrolled dan gaat de de rest mee scrollen.
def yscroll1(*args):
        if vertrektijdbox.yview() != tussenstopbox.yview() and treinsoortbox.yview() != tussenstopbox.yview() and eindbestemmingbox.yview() != tussenstopbox.yview() and vervoerderbox.yview() != tussenstopbox.yview() and vertrekspoorbox.yview() != tussenstopbox.yview():
            vertrektijdbox.yview_moveto(args[0])
            treinsoortbox.yview_moveto(args[0])
            eindbestemmingbox.yview_moveto(args[0])
            vervoerderbox.yview_moveto(args[0])
            vertrekspoorbox.yview_moveto(args[0])
        scrollbar.set(*args)

        if tussenstopbox.yview() != vertrektijdbox.yview() and eindbestemmingbox.yview() != vertrektijdbox.yview() and treinsoortbox.yview() != vertrektijdbox.yview() and vervoerderbox.yview() != vertrektijdbox.yview() and vertrekspoorbox.yview() != vertrektijdbox.yview():
            tussenstopbox.yview_moveto(args[0])
            eindbestemmingbox.yview_moveto(args[0])
            vervoerderbox.yview_moveto(args[0])
            vertrekspoorbox.yview_moveto(args[0])
            treinsoortbox.yview_moveto(args[0])
        scrollbar.set(*args)

        if treinsoortbox.yview() != eindbestemmingbox.yview() and tussenstopbox.yview() != eindbestemmingbox.yview() and vertrektijdbox.yview() != eindbestemmingbox.yview() and vervoerderbox.yview() != eindbestemmingbox.yview() and vertrekspoorbox.yview() != eindbestemmingbox.yview():
            tussenstopbox.yview_moveto(args[0])
            vertrektijdbox.yview_moveto(args[0])
            vervoerderbox.yview_moveto(args[0])
            vertrekspoorbox.yview_moveto(args[0])
            treinsoortbox.yview_moveto(args[0])
        scrollbar.set(*args)

        if eindbestemmingbox.yview() != treinsoortbox.yview() and tussenstopbox.yview() != treinsoortbox.yview() and vertrektijdbox.yview() != treinsoortbox.yview() and vervoerderbox.yview() != treinsoortbox.yview() and vertrekspoorbox.yview() != treinsoortbox.yview():
            tussenstopbox.yview_moveto(args[0])
            vertrektijdbox.yview_moveto(args[0])
            vervoerderbox.yview_moveto(args[0])
            vertrekspoorbox.yview_moveto(args[0])
            eindbestemmingbox.yview_moveto(args[0])
        scrollbar.set(*args)

        if vertrekspoorbox.yview() != vervoerderbox.yview() and tussenstopbox.yview() != vervoerderbox.yview() and vertrektijdbox.yview() != vervoerderbox.yview() and eindbestemmingbox.yview() != vervoerderbox.yview() and treinsoortbox.yview() != vervoerderbox.yview():
            tussenstopbox.yview_moveto(args[0])
            vertrektijdbox.yview_moveto(args[0])
            treinsoortbox.yview_moveto(args[0])
            vertrekspoorbox.yview_moveto(args[0])
            eindbestemmingbox.yview_moveto(args[0])
        scrollbar.set(*args)

        if vervoerderbox.yview() != vertrekspoorbox.yview() and tussenstopbox.yview() != vertrekspoorbox.yview() and vertrektijdbox.yview() != vertrekspoorbox.yview() and eindbestemmingbox.yview() != vertrekspoorbox.yview() and treinsoortbox.yview() != vertrekspoorbox.yview():
            tussenstopbox.yview_moveto(args[0])
            vertrektijdbox.yview_moveto(args[0])
            treinsoortbox.yview_moveto(args[0])
            vervoerderbox.yview_moveto(args[0])
            eindbestemmingbox.yview_moveto(args[0])
        scrollbar.set(*args)


label = Label(master=root, text='', height=2, bg='#FFCC18')
label.pack()
#Frame
buttonFrame = Frame(root)
buttonFrame.pack(fill=X, side=LEFT)

#Vertrektijden box
vertrektijdbox = Listbox(buttonFrame, bg='#FFCC18', fg='#000066', yscrollcommand=yscroll1)
vertrektijdbox.config(font=("Calibri", 12, 'bold'))
vertrektijdbox.grid(row=0, column=0, sticky=W+E)
#Eindbestemming box
eindbestemmingbox = Listbox(buttonFrame, bg='#FFCC18', fg='#000066', yscrollcommand=yscroll1)
eindbestemmingbox.config(font=("Calibri", 12, 'bold'))
eindbestemmingbox.grid(row=0, column=2, sticky=W+E)
#Treinsoort box
treinsoortbox = Listbox(buttonFrame, bg='#FFCC18', fg='#000066', yscrollcommand=yscroll1)
treinsoortbox.config(font=("Calibri", 12, 'bold'))
treinsoortbox.grid(row=0, column=3, sticky=W+E)
#Vervoerder box
vervoerderbox = Listbox(buttonFrame, bg='#FFCC18', fg='#000066', yscrollcommand=yscroll1)
vervoerderbox.config(font=("Calibri", 12, 'bold'))
vervoerderbox.grid(row=0, column=4, sticky=W+E)
#Vertrekspoor box
vertrekspoorbox = Listbox(buttonFrame, bg='#FFCC18', fg='#000066', yscrollcommand=yscroll1)
vertrekspoorbox.config(font=("Calibri", 12, 'bold'))
vertrekspoorbox.grid(row=0, column=5, sticky=W+E)
#Tussenstop box
tussenstopbox = Listbox(buttonFrame, bg='#FFCC18', fg='#000066', yscrollcommand=yscroll1)
tussenstopbox.config(font=("Calibri", 12, 'bold'))
tussenstopbox.grid(row=0, column=6, sticky=W+E)

buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
root.mainloop()
