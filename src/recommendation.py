import config
from loader import load_attractions
from scorer import score_places
from distance import haversine
from schedule import is_place_open_for_visit, estimated_travel_time, minutes_to_time

places=load_attractions("../data/attraction_sites.json")

rating_sorted_places=score_places(config.USER_LAT, config.USER_LONG, places)


def build_itenary():
    visited_set=set()
    for day in range(config.NUM_DAYS):
        curr_time=config.START_TIME
        curr_lat=config.USER_LAT
        curr_long=config.USER_LONG
        print("Day ",day+1," itinerary")
        for place in rating_sorted_places:
            if(place['name']   in visited_set):
                continue
            distance=haversine(curr_lat,curr_long,place["latitude"],place["longitude"])
            travel_time = estimated_travel_time(distance)
            can_visit, start_time,end_time = is_place_open_for_visit(place,curr_time + travel_time)
            if(can_visit):
                if (end_time > config.DAY_END_TIME):  # ← add this check
                    continue
                print(place["name"])
                print("Start at : ", minutes_to_time(start_time))
                print("End at : ", minutes_to_time(end_time))
                curr_lat=place["latitude"]
                curr_long=place["longitude"]
                curr_time=end_time
                visited_set.add(place['name'])
            if(curr_time>=config.DAY_END_TIME):
                print("End of day ",day+1)
                break
