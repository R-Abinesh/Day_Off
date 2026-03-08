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