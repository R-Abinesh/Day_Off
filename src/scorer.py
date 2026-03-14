from cairo import Filter
import config
from distance import haversine
from config import DISTANCE_WEIGHT, RATING_WEIGHT, MAX_RATING


def normalize_distance(distance, max_distance):
    if max_distance == 0:
        return 1
    return 1 - (distance / max_distance)


def normalize_rating(rating):
    return rating / MAX_RATING


def score_places(user_lat, user_lon, places):

    # Step 1: Calculate distance for each place
    for place in places:
        distance = haversine(
            user_lat,
            user_lon,
            place["latitude"],
            place["longitude"]
        )
        place["distance_km"] = distance

    # Step 2: Find maximum distance
    max_distance = max(place["distance_km"] for place in places)

    # Step 3: Compute weighted score
    for place in places:
        distance_score = normalize_distance(
            place["distance_km"],
            max_distance
        )

        rating_score = normalize_rating(place["rating"])

        final_score = (
            DISTANCE_WEIGHT * distance_score +
            RATING_WEIGHT * rating_score
        )

        place["score"] = round(final_score, 4)

    # Step 4: Sort by score (highest first)
    ranked = sorted(
        places,
        key=lambda x: x["score"],
        reverse=True
    )
    return ranked



def score_restaurants(curr_lat, curr_lon, next_lat, next_lon, restaurants, active_meal):
    ### What's happening step by step
    """Filter by meal type (only lunch restaurants during lunch window)
            ↓
        Calculate detour cost for each
        (current → restaurant → next attraction) - (current → next attraction)
            ↓
        Filter by MAX_DETOUR_KM → if empty, try MAX_DETOUR_KM_FALLBACK
            ↓
        Score = DISTANCE_WEIGHT × detour_score + RATING_WEIGHT × rating_score
            ↓
        Return sorted list — best restaurant at index [0]
    """
    # Step 1: filter by meal type
    eligible = [r for r in restaurants if active_meal in r["meal_type"]]
    
    if not eligible:
        return []

    # Step 2: calculate detour cost for each restaurant
    direct_distance = haversine(curr_lat, curr_lon, next_lat, next_lon)

    for r in eligible:
        r_lat, r_lon = r["latitude"], r["longitude"]
        
        # distance from current position to restaurant
        to_restaurant = haversine(curr_lat, curr_lon, r_lat, r_lon)
        
        # distance from restaurant to next attraction
        to_next = haversine(r_lat, r_lon, next_lat, next_lon)
        
        # extra km added vs going directly
        detour_cost = (to_restaurant + to_next) - direct_distance
        
        r["detour_cost"] = round(detour_cost, 4)
        r["distance_km"] = round(to_restaurant, 4)

    # Step 3: filter by detour threshold (progressive radius)
    within_limit = [r for r in eligible if r["detour_cost"] <= config.MAX_DETOUR_KM]
    
    if not within_limit:
        # expand to fallback radius
        within_limit = [r for r in eligible if r["detour_cost"] <= config.MAX_DETOUR_KM_FALLBACK]

    if not within_limit:
        return []

    # Step 4: normalize detour cost
    max_detour = max(r["detour_cost"] for r in within_limit)

    for r in within_limit:
        detour_score  = 1 - (r["detour_cost"] / max_detour) if max_detour > 0 else 1
        rating_score  = normalize_rating(r["rating"])
        r["score"]    = round((DISTANCE_WEIGHT * detour_score) + (RATING_WEIGHT * rating_score), 4)

    # Step 5: sort by score
    return sorted(within_limit, key=lambda x: x["score"], reverse=True)