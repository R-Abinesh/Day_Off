import config
from loader import load_attractions, load_restaurants
from scorer import score_places, score_restaurants
from distance import haversine
from schedule import is_place_open_for_visit, estimated_travel_time, minutes_to_time, get_active_meal_window

places = load_attractions("../data/attraction_sites.json")
restaurants = load_restaurants("../data/restaurants.json")
rating_sorted_places = score_places(config.USER_LAT, config.USER_LONG, places)


def schedule_meal(curr_lat, curr_long, curr_time, active_meal, next_place, meals_done):
    if meals_done[active_meal]:
        return None, curr_time

    # Use next attraction for detour calculation, fallback to user origin
    if next_place:
        next_lat, next_long = next_place["latitude"], next_place["longitude"]
    else:
        next_lat, next_long = config.USER_LAT, config.USER_LONG

    scored = score_restaurants(curr_lat, curr_long, next_lat, next_long, restaurants, active_meal)

    if not scored:
        print(f"  ⚠️  No restaurant found for {active_meal}.")
        choice = input("     [1] Skip meal  [2] Pick nearest anyway: ").strip()
        if choice == "2":
            eligible = [r for r in restaurants if active_meal in r["meal_type"]]
            if not eligible:
                meals_done[active_meal] = True
                return None, curr_time
            scored = sorted(eligible, key=lambda x: haversine(curr_lat, curr_long, x["latitude"], x["longitude"]))
        else:
            meals_done[active_meal] = True
            return None, curr_time

    restaurant = scored[0]
    travel_time = estimated_travel_time(restaurant["distance_km"])
    arrival = curr_time + travel_time

    # Get meal-specific duration
    duration = restaurant.get("meal_durations", {}).get(active_meal) or restaurant.get("visit_duration", 45)
    can_visit, start_time, end_time = is_place_open_for_visit(
        {**restaurant, "visit_duration": duration}, arrival
    )

    if not can_visit:
        print(f"  ⚠️  {restaurant['name']} not available for {active_meal}.")
        meals_done[active_meal] = True
        return None, curr_time

    wait = start_time - arrival
    print(f"  {minutes_to_time(start_time)} – {minutes_to_time(end_time)}  "
          f"🍽️  {restaurant['name']} ({active_meal})"
          f"  (🚗 {travel_time}min{f'  ⏳ {wait}min wait' if wait > 0 else ''})")

    meals_done[active_meal] = True
    return restaurant, end_time


def build_itenary():
    visited_set = set()

    for day in range(config.NUM_DAYS):
        curr_time = config.START_TIME
        curr_lat  = config.USER_LAT
        curr_long = config.USER_LONG

        meals_done = {meal: False for meal in config.MEAL_WINDOWS}  # resets every day

        print("\nDay ", day + 1, " itinerary")
        print("=" * 40)

        for place in rating_sorted_places:
            if place["name"] in visited_set:
                continue

            # Check and schedule meal before next attraction
            active_meal = get_active_meal_window(curr_time)
            if active_meal and not meals_done[active_meal]:
                restaurant, curr_time = schedule_meal(
                    curr_lat, curr_long, curr_time, active_meal, place, meals_done
                )
                if restaurant:
                    curr_lat  = restaurant["latitude"]
                    curr_long = restaurant["longitude"]

            # Schedule attraction
            distance    = haversine(curr_lat, curr_long, place["latitude"], place["longitude"])
            travel_time = estimated_travel_time(distance)
            can_visit, start_time, end_time = is_place_open_for_visit(place, curr_time + travel_time)

            if can_visit:
                if end_time > config.DAY_END_TIME:
                    continue

                print(place["name"])
                print("Start at : ", minutes_to_time(start_time))
                print("End at   : ", minutes_to_time(end_time))

                curr_lat  = place["latitude"]
                curr_long = place["longitude"]
                curr_time = end_time
                visited_set.add(place["name"])

                if curr_time >= config.DAY_END_TIME:
                    print("End of day ", day + 1)
                    break

        # Schedule dinner after attractions if still in dinner window
        active_meal = get_active_meal_window(curr_time)
        if active_meal and not meals_done[active_meal]:
            next_place = get_next_unvisited(visited_set)
            schedule_meal(curr_lat, curr_long, curr_time, active_meal, next_place, meals_done)


build_itenary()