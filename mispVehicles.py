from pymisp import MISPEvent
from pymisp import MISPObject
import json
import os.path
import json

event = MISPEvent()

event.info = 'MISP event for stolen cars'  # Required
event.distribution = 0  # Optional, defaults to MISP.default_event_distribution in MISP config
event.threat_level_id = 2  # Optional, defaults to MISP.default_event_threat_level in MISP config
event.analysis = 1  # Optional, defaults to 0 (initial analysis)

# VEHICLE
def createMispVehicule(): # create misp object vehicle
    mispObject = MISPObject('vehicle', standalone=False)
    return mispObject

def addComment(mispObject, comment): # add number report comment to mispobject
    mispObject.comment = 'Rapport number ' + comment

def addAttributeMispVehicle(mispObject, attr, val): # add val to attr in mispObject
    mispObject.add_attribute(attr, value=val)

def addMispVehicle(mispObject): # add mispObject to event
    event.add_object(mispObject)

# GEOLOCATION
def createMispGeolocation(): # create misp object geolocation
    mispObject2 = MISPObject('geolocation', standalone=False)
    return mispObject2

def addAttributeMispGeolocation(mispObject2, attr, val): # add val to attr in mispObject
    mispObject2.add_attribute(attr, value=val)

def addMispGeolocation(mispObject2): # add mispObject to event
    event.add_object(mispObject2)


# SAVE IN JSON FILE AND UPDATE IF THE FILE EXIST
def printEvent():
    if not os.path.isfile("data.json"): # If the file doesn't exit, we create it and we write it
        print (" Création du fichier et écriture des données !")
        with open("data.json", "w") as fichier:
        	fichier.write(event.to_json(indent=2)) # write event in data.json
    else: # else the file exist, we update this file
        print(" Json Update !")
        with open("data2.json", "w") as json_file:
            json_file.write(event.to_json(indent=2)) # write new event in data2.json
        if os.path.isfile("data2.json"): # If the file data2.json exist
            with open("data.json") as old_data:
                dic1 = json.load(old_data) # Load in memory data.json
            with open("data2.json") as new_data:
                dic2 = json.load(new_data) # Load in memory data2.json
            dic1.update(dic2) # Update the old file (data.json) with the new file (data2.json)
            with open("data.json", "w") as update:
            	json.dump(dic1, update, indent=2) # write update event in data.json
        if os.path.exists("data2.json"):
          os.remove("data2.json") # remove update file (data2.json)
        else:
          print("The file does not exist")
