import time
import json

"""
Wird aufgerufen, wenn der Nutzer etwas an den eigenen Pflanzen ändert (Name, Typ, Giess-Status 
zurücksetzen, Pflanze löschen odedr neue Pflanze hinzufügen). Diese Änderungen werden in db-garden 
aktualisiert und gespeichert. Damit bekannt ist, welche der Pflanzen genau gändert werden muss, ist 
die ID der eigenen Pflanze immer im Formular enthalten. Das Formularfeld "action" beschreibt welche
Aktion der Benutzer angefordert hat.
"""
def edit_garden(request, db_garden):
    # Pflanzen-Name oder -Typ ändern
    if request.form["action"] == "edit_plant":
        db_garden[request.form['id']]["name"] = request.form['name']
        db_garden[request.form['id']]["type"] = request.form['type']

    # Pflanze löschen
    elif request.form["action"] == "delete_plant":
        db_garden.pop(request.form['id'])

    # Giess-Status zurücksetzen
    elif request.form["action"] == "reset_water":
        db_garden[request.form['id']]["last_water"] = time.time()

    # neue Pflanze hinzufügen mit anpassbarem default Inhalt
    # bekommt die nächstgrössere ID (last_id +1) aus allen aktuellen Pflanzen, damit es keine
    # Konflikte gibt und speichert diese als last_id
    elif request.form["action"] == "add_plant":
        id_new_plant = str(int(db_garden["last_id"]) + 1)
        db_garden[id_new_plant] = {"name": "Neue Pflanze",
                                   "type": "0",
                                   "last_water": time.time()}
        db_garden["last_id"] = id_new_plant

    # Speichern der Änderungen im db_garden json-File
    with open('data/db_garden.json', 'w') as open_file:
        json_als_string = json.dumps(db_garden, indent=4)
        open_file.write(json_als_string)

def edit_type(request, db_plants_info):
    # Typ-Name oder Giesshäufigkeit ändern
    if request.form["action"] == "edit_type":
        db_plants_info[request.form["id"]]["name"] = request.form['name']
        db_plants_info[request.form["id"]]["water_freq"] = int(request.form['water_freq'])

    # Pflanze löschen
    elif request.form["action"] == "delete_type":
        db_plants_info.pop(request.form["id"])

    # neuen Typ hinzufügen mit anpassbarem default Inhalt
    # bekommt die nächstgrössere ID (last_id +1) aus allen aktuellen Typen, damit es keine
    # Konflikte gibt und speichert diese als last_id
    elif request.form["action"] == "add_type":
        id_new_type = str(int(db_plants_info["last_id"]) + 1)
        db_plants_info[id_new_type] = {"name": "Neuer Typ",
                                        "water_freq": 0,
                                        }
        db_plants_info["last_id"] = id_new_type

    # Speichern der Änderungen im db_plants json-File
    with open('data/db_plants.json', 'w') as open_file:
        json_als_string = json.dumps(db_plants_info, indent=4)
        open_file.write(json_als_string)