import config

def time_to_minutes(time_str):
    hours,minutes = map(int,time_str.split(':'))
    return int(hours*60 + minutes)

def estimated_travel_time(distance_km):
    return int((distance_km / config.CITY_SPEED) * 60)

def is_place_open(time,arrival_time):
    if(time_to_minutes(time['start'])<=arrival_time and time_to_minutes(time['end'])>=arrival_time):
        return True
    return False

def is_place_open_for_visit(place,arrival_time):
    #calculate the time between user arrival and place closing time
    for time in place['open_hours']:
        time_available_for_user=time_to_minutes(time['end'])-arrival_time
        # print(time_available_for_user)
        if(is_place_open(time,arrival_time) and time_available_for_user>=place['visit_duration']):
            return True, arrival_time
    return False, None



# #If you want to use this module, then call is_place_open_for_visit function with place and arrival time in minutes as arguments. It will return true if the place is open for visit and false otherwise.
# places=load_attractions("../data/attraction_sites.json")
# for place in places:
#     print(place['name'])
#     if(is_place_open_for_visit(place,1020)):
#         print("Yes, the place is open for visit")
#     else:
#         print("No, the place is not open for visit")

