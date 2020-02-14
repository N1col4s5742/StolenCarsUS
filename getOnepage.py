from urllib.request import urlopen
import bs4 as BeautifulSoup
import mispVehicles

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
def extractInfosVehicle(vehicleLink, state):
    # form of vehicleLink : /Report/View/325?loadLayout=False
    mispVehicle = mispVehicles.createMispVehicule()
    mispGeolocation = mispVehicles.createMispGeolocation()

    print("\t Analyze new vehicle :")
    html = urlopen('https://www.stolencar.com' + str(vehicleLink)).read()
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser") #open webpage

    for img in soup.find_all('img', src=True):  # get url image
        print(img['alt'], " : ", img['src'])
        mispVehicle.add_attribute("image-url", value="https://www.stolencar.com"+img['src'])

    for p in soup.find_all('p'):
        # print("--")
        if "<p>" in str(p): # white line
            nameFeature = extractFeatureName(p, "<p>")
        elif '<p style="background:#f0f0f0;">' in str(p): # grey line
            nameFeature = extractFeatureName(p, '<p style="background:#f0f0f0;">')

        feature = (str(p).split("<span>")[1].strip()).split("</span>")[0].strip() # split feature of the line
        if feature != "": #feature doesn't empty
            print(nameFeature, " : ", feature)
            if str(nameFeature) in websiteToMisp:
                mispVehicles.addAttributeMispVehicle(mispVehicle,websiteToMisp[nameFeature],feature); #add attribute ton mispvehicle
                if nameFeature == "Report #":
                    mispVehicles.addComment(mispVehicle, feature) # Report's number as a comment
            if str(nameFeature) in websiteToMisp2:
                if nameFeature == "Date":
                    obj_attr = mispGeolocation.add_attribute("last-seen", value=feature) # add last seen as GeoLocation
            if str(nameFeature) in websiteToMisp3:
                mispVehicles.addAttributeMispGeolocation(mispGeolocation, websiteToMisp3[nameFeature], feature) # add attribute about GeoLocation in mispVehicles
        if "Neighborhood" in str(p):  # any interesting info after this feature
            break

    mispVehicle.add_attribute("state", value=state) # add state of vehicle to mispVehicle
    mispVehicle.add_reference(obj_attr.uuid, 'last-seen-at', 'Date of last seen the vehicle') # add a reference to mispVehicle and last-seen
    mispVehicles.addMispVehicle(mispVehicle) # add misp object mispVehicle completed to its related event
    mispVehicles.addMispGeolocation(mispGeolocation) # add misp object mispGeolocation completed to its related event
    print("State : ", state)

# print event linked to mispVehiclesf
def printMispEvent():
    mispVehicles.printEvent()

# extractInfosVehicle(500, "stolen")
