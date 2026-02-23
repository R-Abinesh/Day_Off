import json
import math

# -------------------------
# 1. Load attractions
# -------------------------
with open("attraction_sites.json", "r") as file:
    attractions = json.load(file)


# -------------------------
# 2. Haversine function
# -------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dLon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# -------------------------
# 3. User location input
# -------------------------
user_lat = float(input("Enter your latitude: "))
user_lon = float(input("Enter your longitude: "))


# -------------------------
# 4. Calculate distances
# -------------------------
for attraction in attractions:
    distance = haversine(
        user_lat,
        user_lon,
        attraction["latitude"],
        attraction["longitude"],
    )
    attraction["distance_km"] = round(distance, 2)


# -------------------------
# 5. Sort by distance
# -------------------------
attractions.sort(key=lambda x: x["distance_km"])


# -------------------------
# 6. Show top 5
# -------------------------
print("\nTop 5 nearest attractions:\n")

for attraction in attractions[:5]:
    print(f"{attraction['name']} - {attraction['distance_km']} km")
