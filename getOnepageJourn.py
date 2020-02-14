# This file is an alternative to getOnePage.py.
# If you considere that you have to pool on the stolen car's website very regularly (1 time per dey for example), you can use it instead of getOnepage.py

from urllib.request import urlopen
import bs4 as BeautifulSoup
import mispVehiclesJourn
import json
from pymisp import MISPEvent
from pymisp import MISPObject

def extractFeatureName(variable, tagToSplit): # return feature's name according to the tag to split
    return (str(variable).split("<span>")[0].strip()).split(tagToSplit)[1].strip()

# dictionary for correspondance between website words and misp words
websiteToMisp =	{
    "Vehicle Image": "image-url",
    "Report #": "description",
    "Make": "make",
    "Model": "model",
    "Year": "date-first-registration",
    "Exterior Color": "exterior color",
    "Interior Color": "interior color",
    "Type": "type",
    "License State": "state",
    "License Plate #": "license-plate-number",
    "VIN #": "vin"
}

websiteToMisp2 = {
    "Date": "last-seen",
}

websiteToMisp3 = {
    "Street": "address",
    "City, State": "city",
    "Zip Code": "zipcode",
    "Neighborhood": "neighborhood"
}

# extract informations about vehicle which is referenced by vehicleLink and his state
def extractInfosVehicle(vehicleLink, state, jsonExist):
    # form of vehicleLink : /Report/View/325?loadLayout=False
    mispVehicle = mispVehiclesJourn.createMispVehicule()
    mispGeolocation = mispVehiclesJourn.createMispGeolocation()

    print("\t Analyze new vehicle :")
    html = urlopen('https://www.stolencar.com' + str(vehicleLink)).read()
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
    report = ""

    for img in soup.find_all('img', src=True):  # get url image
        print(img['alt'], " : ", img['src'])
        mispVehicle.add_attribute("image-url", value="https://www.stolencar.com"+img['src'])

    for p in soup.find_all('p'):
        # print("--")
        if "<p>" in str(p):
            nameFeature = extractFeatureName(p, "<p>")
        elif '<p style="background:#f0f0f0;">' in str(p):
            nameFeature = extractFeatureName(p, '<p style="background:#f0f0f0;">')

        feature = (str(p).split("<span>")[1].strip()).split("</span>")[0].strip()
        if feature != "": #feature doesn't empty
            print(nameFeature, " : ", feature)
            if str(nameFeature) in websiteToMisp:
                mispVehiclesJourn.addAttributeMispVehicle(mispVehicle,websiteToMisp[nameFeature],feature);
                if nameFeature == "Report #":
                    mispVehiclesJourn.addComment(mispVehicle, feature)
                    report = feature
            if str(nameFeature) in websiteToMisp2:  # any interesting info after this feature
                # mispVehiclesJourn.addAttributeMispGeolocation(mispGeolocation, websiteToMisp2[nameFeature], feature)
                if nameFeature == "Date":
                    obj_attr = mispGeolocation.add_attribute("last-seen", value=feature)
            if str(nameFeature) in websiteToMisp3:
                mispVehiclesJourn.addAttributeMispGeolocation(mispGeolocation, websiteToMisp3[nameFeature], feature)
        if "Neighborhood" in str(p):  # any interesting info after this feature
            break

    mispVehicle.add_attribute("state", value=state)
    mispVehicle.add_reference(obj_attr.uuid, 'last-seen-at', 'Date of last seen the vehicle')

    print("State : ", state)
    if jsonExist == False:
        print("Json n'existe pas")
        mispVehiclesJourn.addMispVehicle(mispVehicle)
        mispVehiclesJourn.addMispGeolocation(mispGeolocation)
    else:
        print("Json existe")
        modifyExistingJson(report, state, mispVehicle, mispGeolocation)


def printMispEvent():
    mispVehiclesJourn.saveEvent()

# Function to modify an existing json if the number of report exists, and the state has changed.
# If vehicle doesn't exist, addNewObjectsExistingJson is called to add it in json
def modifyExistingJson(rapportNumber, stateVehicle, mispVehicle, mispGeolocation):
    with open('data.json') as json_file:
        data = json.load(json_file)
        jsonHasChanged = False
        vehicleFound = False
        for key in data["Object"]:
            if key["name"] == "vehicle":
                if rapportNumber in key["Attribute"][1]["value"] and \
                        (key["Attribute"][len(key["Attribute"])-1]["value"] != stateVehicle):
                    print("--> Json existant, mais changement d'état du véhicule")
                    jsonHasChanged = True
                    key["Attribute"][len(key["Attribute"]) - 1]["value"] = stateVehicle
                elif rapportNumber in key["Attribute"][1]["value"]:
                    vehicleFound = True

                # print(key["Attribute"][1]["value"])
                # print(key["Attribute"][len(key["Attribute"])-1]["value"])

        if jsonHasChanged:
            print("A changé !")
            with open("data.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=2)
        elif vehicleFound == False:
            print("-->Json existant, mais nouveau véhicule à ajouter")
            addNewObjectsExistingJson(mispVehicle, mispGeolocation)
        else:
            print("N'a pas changé !")

# Function to add new vehicle and related geolocation to existing json
def addNewObjectsExistingJson(mispVehicle, mispGeolocation):
    existing_event = MISPEvent()
    existing_event.load_file('data.json')
    existing_event.add_object(mispVehicle)
    existing_event.add_object(mispGeolocation)
    open("data.json", 'a').close()
    with open("data.json", "w") as fichier:
        fichier.write(existing_event.to_json(indent=2))  # écriture de l'évènement
    print("Nouveau véhicule ajouté au json existant")

