from urllib.request import urlopen
import bs4 as BeautifulSoup
from math import *
from getOnepageJourn import extractInfosVehicle
from getOnepageJourn import printMispEvent
import os


if __name__ == '__main__':
    html = urlopen('https://www.stolencar.com/Report/Search?&p=1').read()
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
    # print(soup)
    jsonExist = False
    if os.path.isfile("data.json"):  # file doesn't exist
        jsonExist = True
    else:
        jsonExist = False

    nb = soup.findAll("sub")  # tag where is the nb total vehicle in database
    nbTotalVehicles = (str(nb).split("(")[1]).split(" ")[0]  # get only nb total
    nbTotalAnalyzed = 0
    print(" -- Nb total de véhicules = ", nbTotalVehicles, " --")

    # for i in range (1, ceil(int(nbTotalVehicles)/25)+1):
    for i in range(2, 4):
        print(" ***** Page ", i, " *****");
        urlToExplore = 'https://www.stolencar.com/Report/Search?&p=' + str(i)
        html = urlopen(urlToExplore).read()
        soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
        for rows in soup.findAll("article"):  # get just articles = vehicles
            for vehicle in rows.findAll("div", {"class": "col-sm-3"}):  # delete useless info
                url = ""  # allow to know if an url is found for vehicle
                for a in vehicle.find_all('a', href=True):  # get only href vehicle
                    url = a['href']
                    # print(a['href']);
                recovered = vehicle.find('b', style="color: red")  # recovered vehicle
                if recovered == None and url != "":
                    # print("Stolen")
                    extractInfosVehicle(url, "Stolen", jsonExist)
                    url = ""
                    nbTotalAnalyzed = nbTotalAnalyzed + 1
                elif recovered != None and url != "":
                    # print("Recovered")
                    extractInfosVehicle(url, "Recovered", jsonExist)
                    url = ""
                    nbTotalAnalyzed = nbTotalAnalyzed + 1
        print("\n")


    print(" * * * * * * * * * * * * * * * ")
    print("Nombre total de véhicules analysés = " + str(nbTotalAnalyzed))

    if not jsonExist:  # file doesn't exist
        printMispEvent()
        print("Nouveau json créée ! ")
    else:
        print("Le fichier existe déjà, update de l'existant ! ")
