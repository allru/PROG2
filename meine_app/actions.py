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
    with open('db_garden.json', 'w') as open_file:
        json_als_string = json.dumps(db_garden, indent=4)
        open_file.write(json_als_string)
