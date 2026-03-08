from loader import load_attractions
from scorer import score_places
import config
from distance import haversine
from schedule import is_place_open_for_visit, estimated_travel_time

places=load_attractions("../data/attraction_sites.json")

rating_sorted_places=score_places(config.USER_LAT, config.USER_LONG, places)

for place in rating_sorted_places:
    distance = haversine(
            config.USER_LAT,
            config.USER_LONG,
            place["latitude"],
            place["longitude"]
        )
    travel_time = estimated_travel_time(distance)
    can_visit, start_time = is_place_open_for_visit(place,config.START_TIME + travel_time)
    if can_visit:
        print(place["name"], place["score"])


