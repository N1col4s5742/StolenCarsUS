from pymisp import MISPEvent
from pymisp import MISPObject

event = MISPEvent()

event.info = 'MISP event for stolen cars'  # Required
event.distribution = 0  # Optional, defaults to MISP.default_event_distribution in MISP config
event.threat_level_id = 2  # Optional, defaults to MISP.default_event_threat_level in MISP config
event.analysis = 1  # Optional, defaults to 0 (initial analysis)


def createMispVehicule(): # create misp object vehicle
    mispObject = MISPObject('vehicle', standalone=False)
    return mispObject

def addComment(mispObject, comment): # add comment to mispobject
    mispObject.comment = 'Rapport number ' + comment

def addAttributeMispVehicle(mispObject, attr, val): # add val to attr in mispObject
    mispObject.add_attribute(attr, value=val)

def addMispVehicle(mispObject): # add mispObject to event
    event.add_object(mispObject)

# def printEvent(): # print event
#     print(event.to_json(indent=2))

# GEOLOCATION
def createMispGeolocation(): # create misp object geolocation
    mispObject2 = MISPObject('geolocation', standalone=False)
    return mispObject2

def addAttributeMispGeolocation(mispObject2, attr, val): # add val to attr in mispObject
    mispObject2.add_attribute(attr, value=val)

def addMispGeolocation(mispObject2): # add mispObject to event
    event.add_object(mispObject2)

# SAVE IN JSON FILE
def saveEvent():
    open("data.json", 'a').close() # ouverture en lecture pour supprimer les données déjà enregistré dans le fichier ou créer le fichier si il n'existe pas
    with open("data.json", "w") as fichier:
    	fichier.write(event.to_json(indent=2)) # écriture de l'évènement

def createExistingEvent():
    existing_event = MISPEvent()
    existing_event.load_file('data.json')
    return existing_event
