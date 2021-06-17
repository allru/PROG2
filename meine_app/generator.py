import time

def generate_plants_info(db_plants, db_garden):
    plants_info = []
    for plant in db_garden:

        water_freq = db_plants[plant["type"]]["water_freq"]
        curr_time = time.time()
        last_time = plant["last_water"]

        water_countdown = int(round( water_freq-(curr_time-last_time)/60 ))

        if water_countdown > 0:
            water_countdown_color = "green"
        elif water_countdown > -2:
            water_countdown_color = "orange"
        else:
            water_countdown_color = "red"

        if water_freq == 1 or water_freq == -1:
            water_freq = str(water_freq) + " Minute"
        else:
            water_freq = str(water_freq) + " Minuten"

        if water_countdown == 1 or water_countdown == -1:
            water_countdown = str(water_countdown) + " Minute"
        else:
            water_countdown = str(water_countdown) + " Minuten"



        plants_info.append({
            "name": plant["name"],
            "type": db_plants[plant["type"]]["name"],
            "water_freq": water_freq,
            "water_countdown": water_countdown,
            "water_countdown_color": water_countdown_color
        })
    return plants_info


def generate_type_select(db_plants):
    type_select = []
    for plant in db_plants.values():
        type_select.append(plant["name"])
    return type_select