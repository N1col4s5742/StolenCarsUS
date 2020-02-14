from urllib.request import urlopen
import bs4 as BeautifulSoup
from math import *
from getOnepage import extractInfosVehicle
from getOnepage import printMispEvent


if __name__ == '__main__':
    html = urlopen('https://www.stolencar.com/Report/Search?&p=1').read()
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
    # print(soup)

    nb = soup.findAll("sub")  # tag where is the nb total vehicle in database
    nbTotalVehicles = (str(nb).split("(")[1]).split(" ")[0]  # get only nb total
    print(" -- Nb total de véhicules = ", nbTotalVehicles, " --")

	# !!! Always 1 for the first range !!!
    # for i in range (1, ceil(int(nbTotalVehicles)/25)+1): #loop on all pages
    for i in range(1, 3): #loop [1,j[
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
                    extractInfosVehicle(url, "Stolen")
                    url = ""
                elif recovered != None and url != "":
                    # print("Recovered")
                    extractInfosVehicle(url, "Recovered")
                    url = ""
        print("\n")

    print(" * * * * * * * * * * * * * * * ")
    printMispEvent()
