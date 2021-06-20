import time
import re

"""
Generieren der plant-info, die in HTML genutzt wird, um meine Pflanzen anzuzeigen.
Erstelle hier eine Liste mit id, name, type, water_freq, water_countdown_nr, water_countdown und water_countdown_color 
für jede meiner Pflanzen, auf Basis der beiden json Datengrundlagen und der aktuellen Zeit.
Die last_id in db_garden wird hier übersprungen, ist aber nötig (siehe actions.py).
"""
def generate_plants_info(db_plants, db_garden):
    plants_info = []

    for plant_key in db_garden.keys():
        if plant_key == "last_id":
            continue
        plant = db_garden[plant_key]

        # Berechne Zeit (in Minuten) bis zum nächsten empfohlenen Giesszeitpunkt aufgrund der
        # Giesshäufigkeit des Pflanzentyps, der aktuellen Zeit und dem Zeitpunkt des letzten Giessens
        # (negativ = zu spät)
        water_freq = db_plants[plant["type"]]["water_freq"]
        curr_time = time.time()
        last_time = plant["last_water"]
        water_countdown_nr = int(round( water_freq-(curr_time-last_time)/60 ))


        # Einfärbung der Zeit nach Dringlichkeit des Giessens
        if water_countdown_nr > 0:
            water_countdown_color = "green"
        elif water_countdown_nr > -2:
            water_countdown_color = "orange"
        else:
            water_countdown_color = "red"

        # Anpassung Schreibweise Minuten Plural/Singular
        if water_freq == 1 or water_freq == -1:
            water_freq = str(water_freq) + " Minute"
        else:
            water_freq = str(water_freq) + " Minuten"

        if water_countdown_nr == 1 or water_countdown_nr == -1:
            water_countdown = str(water_countdown_nr) + " Minute"
        else:
            water_countdown = str(water_countdown_nr) + " Minuten"


        # gewonnene Infos zur Liste hinzufügen, pro Pflanze
        plants_info.append({
            "id": plant_key,
            "name": plant["name"],
            "type": plant["type"],
            "water_freq": water_freq,
            "water_countdown_nr": water_countdown_nr,
            "water_countdown": water_countdown,
            "water_countdown_color": water_countdown_color
        })

    # Sortiere Pflanzen-Ansicht nach Giess-Dringlichkeit
    plants_info.sort(key=lambda i: i['water_countdown_nr'])

    return plants_info


"""
Generieren der Inhalte für Dropdown Auswahl der Pflanzenart (Typ) für HTML.
Liste mit Name und ID pro Pflanzentyp. Name für Darstellung, ID für Tracking der Änderungen in der 
db_garden, falls der Pflanzentyp geändert wird (siehe actions.py).
"""
def generate_type_select(db_plants):
    type_select = []
    for element in db_plants.items():

        type_select.append({"id": element[0],
                            "name": element[1]["name"]})

    return type_select
