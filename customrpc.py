import pypresence # the main thing
import time
import os
import json

if not os.path.exists("presets.json"):
    with open("presets.json", "wb") as file:
        json.dump({ # example presets.
        {
            "blank": {
                "appname": "PLAYING/LISTENING/WATCHING [appname]",
                "state": "The first text.",
                "details": "The second text.",
                "type": "can be LISTENING, WATCHING, COMPETING, or PLAYING. if none, defaults to PLAYING.",
                "largeimage": "can be an image added to your art assets or a url.",
                "largeimagetext": "what shows up when a user hovers over.",
                "smallimage": "",
                "smallimagetext": "",
                "button1text": "text that will show for button 1",
                "button1url": "what the button leads to",
                "button2text": "",
                "button2url": ""
            },
            "blank2": {
                "appname": "",
                "state": "",
                "details": "",
                "type": "",
                "largeimage": "",
                "largeimagetext": "",
                "smallimage": "",
                "smallimagetext": "",
                "button1text": "",
                "button1url": "",
                "button2text": "",
                "button2url": ""
            },
        }
        }, file)
        print("Created presets.json. Please add your presets for the Rich Presence and rerun this script!")

with open("presets.json", "rb") as file: # we load the presets
    presets = json.load(file)

selected = {}

prescensereal = pypresence.Client(client_id=1517335804945502329) # default client id. you can change to your own if you wish!
try:
    prescensereal.start()
except pypresence.DiscordNotFound:
    print("Failed to start RPC. Is Discord running?")
    exit()
inpresence = False  

def getActivityType(type):
    if type == "WATCHING":
        return pypresence.ActivityType.WATCHING
    elif type == "LISTENING":
        return pypresence.ActivityType.LISTENING
    elif type == "COMPETING":
        return pypresence.ActivityType.COMPETING
    return pypresence.ActivityType.PLAYING

while True:
    try:
        print("Select from one of the available presets, or CTRL + C to quit:")
        for key in presets.keys():
            print(key)
        userselect = input(">> ")
        
        if userselect in presets.keys():
            selected = presets[userselect]
            currenttime = round(time.time())
            inpresence = True
            print("Starting rpc...")

        while inpresence:
            try:
                activity_kwargs = {
                    "activity_type": getActivityType(selected.get("type", "")),
                    "start": currenttime,
                }

                if selected.get("state"):
                    activity_kwargs["details"] = selected["state"]
                if selected.get("details"):
                    activity_kwargs["state"] = selected["details"]
                if selected.get("appname"):
                    activity_kwargs["name"] = selected["appname"]
                if selected.get("largeimage"):
                    activity_kwargs["large_image"] = selected["largeimage"]
                if selected.get("largeimagetext"):
                    activity_kwargs["large_text"] = selected["largeimagetext"]
                if selected.get("smallimage"):
                    activity_kwargs["small_image"] = selected["smallimage"]
                if selected.get("smallimagetext"):
                    activity_kwargs["small_text"] = selected["smallimagetext"]

                buttons = []
                if selected.get("button1text") and selected.get("button1url"):
                    buttons.append({"label": selected["button1text"], "url": selected["button1url"]})
                if selected.get("button2text") and selected.get("button2url"):
                    buttons.append({"label": selected["button2text"], "url": selected["button2url"]})
                if buttons:
                    activity_kwargs["buttons"] = buttons

                prescensereal.set_activity(**activity_kwargs)
                time.sleep(15) # update every 15 seconds
            except KeyboardInterrupt:
                prescensereal.clear_activity()
                print("Closed RPC.")
                inpresence = False
    
    except KeyboardInterrupt:
        prescensereal.close()
        print("Seeya!")
        exit()