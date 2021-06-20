import json
from flask import Flask
from flask import render_template
from flask import request
from generator import generate_plants_info, generate_type_select
from actions import edit_garden
from actions import edit_type

app = Flask("Meine Pflanzen")


@app.route('/', methods=['GET', 'POST'])
def index():

    # Datengrundlagen laden, 1x alle möglichen Pflanzen (db_plants), 1x meine Pflanzen (db_garden)
    db_plants_info = json.load(open(r"db_plants.json", "r", encoding='utf-8'))
    db_plants = db_plants_info
    db_plants.pop('last_id')
    db_garden = json.load(open(r"db_garden.json", "r", encoding='utf-8'))

    # wenn etwas an meinen Pflanzen geändert wurde, aktualisiert sich db_garden
    if request.method == 'POST':
        edit_garden(request, db_garden)

    # generieren der Pflanzeninfos, die mit HTML auf der Webseite angezeigt werden sollen
    plants_info = generate_plants_info(db_plants, db_garden)
    type_select = generate_type_select(db_plants)

    # Jinja Code im HTML auswerten und an Webseite übermitteln
    return render_template('index.html', plants_info=plants_info, type_select=type_select)


@app.route('/typen-verwalten', methods=['GET', 'POST'])
def typen_verwalten():
    db_plants_info = json.load(open(r"db_plants.json", "r", encoding='utf-8'))

    if request.method == 'POST':
        edit_type(request, db_plants_info)

    db_plants = db_plants_info
    db_plants.pop('last_id')

    return render_template('typen-verwalten.html', db_plants=db_plants)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
