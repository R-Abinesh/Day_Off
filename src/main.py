import json
from scorer import score_places


def load_places(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":

    # Example user location (Coimbatore city center)
    user_lat = 11.0168
    user_lon = 76.9558

    places = load_places("../data/attraction_sites.json")

    ranked_places = score_places(user_lat, user_lon, places)

    print("\nRecommended Attractions:\n")

    for place in ranked_places:
        print(
            f"{place['name']} | "
            f"Distance: {round(place['distance_km'],2)} km | "
            f"Score: {place['score']}"
        )