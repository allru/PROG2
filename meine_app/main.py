import json
from flask import Flask
from flask import render_template
from generator import generate_plants_info, generate_type_select

app = Flask("Meine Pflanzen")

@app.route('/')
def index():

    #load databases of plant definitions and of composition of garden
    db_plants = json.load(open(r"db_plants.json", "r", encoding='utf-8'))
    db_garden = json.load(open(r"db_garden.json", "r", encoding='utf-8'))
    plants_info = generate_plants_info(db_plants, db_garden)
    type_select = generate_type_select(db_plants)

    return render_template('index.html', plants_info=plants_info, type_select=type_select)



if __name__ == "__main__":
    app.run(debug=True, port=5000)