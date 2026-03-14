DISTANCE_WEIGHT = 0.6
RATING_WEIGHT = 0.4
MAX_RATING = 5
CITY_SPEED = 30
USER_LAT = 11.0168
USER_LONG = 76.9558
START_TIME=600
MAX_WAIT_TIME=30
NUM_DAYS=3
DAY_END_TIME=1320

# Meal windows — all times in minutes
MEAL_WINDOWS = {
    "breakfast": {"start": 450,  "end": 570},   # 07:30 – 09:30
    "lunch":     {"start": 720,  "end": 840},   # 12:00 – 14:00
    "snack":     {"start": 930,  "end": 1020},  # 15:30 – 17:00
    "dinner":    {"start": 1140, "end": 1260},  # 19:00 – 21:00
}

MAX_DETOUR_KM          = 5   # initial search radius
MAX_DETOUR_KM_FALLBACK = 15  # expanded radius if no restaurant found within 5km