# 🗺️ Day Off — AI Itinerary Planner

A modular Python system that recommends the best places to visit in a city within a day (or multiple days), considering distance, attraction ratings, travel time, opening hours, and visit duration.

---

## 📁 Project Structure

```
src/
├── main.py               # Entry point
├── config.py             # All configuration constants
├── loader.py             # Load attraction data from JSON
├── distance.py           # Haversine distance calculation
├── scorer.py             # Rank attractions by score
├── schedule.py           # Time feasibility checks
├── recommendation.py     # Core itinerary engine
data/
└── attraction_sites.json # Attraction data
```

---

## ⚙️ Configuration (`config.py`)

| Constant                 | Description                             | Default          |
| ------------------------ | --------------------------------------- | ---------------- |
| `USER_LAT` / `USER_LONG` | User's starting location                | 11.0168, 76.9558 |
| `START_TIME`             | Day start in minutes (540 = 09:00)      | 540              |
| `DAY_END_TIME`           | Day end in minutes (1260 = 21:00)       | 1260             |
| `MAX_WAIT_TIME`          | Max minutes to wait for a place to open | 30               |
| `NUM_DAYS`               | Number of days to plan                  | 3                |
| `CITY_SPEED`             | Average city travel speed (km/h)        | 30               |
| `DISTANCE_WEIGHT`        | Weight for distance in scoring          | 0.6              |
| `RATING_WEIGHT`          | Weight for rating in scoring            | 0.4              |

---

## 🚀 Usage

```bash
cd src
python3 main.py
```

### Example Output

```
Day 1 itinerary
Gedee Car Museum
Start at : 10:04
End at   : 11:34

VOC Park and Zoo
Start at : 11:35
End at   : 13:05
...
```

---

## 📦 Phases

### ✅ Phase 1 — Data Loading

Loads attraction data from a JSON file into Python objects.

Functions added in `loader.py`:

- `load_attractions()` — reads and parses `attraction_sites.json`

---

### ✅ Phase 2 — Attraction Scoring

Ranks attractions using a weighted score based on distance and rating.

Functions added in `scorer.py`:

- `normalize_distance()` — normalizes distance relative to the farthest place
- `normalize_rating()` — normalizes rating out of `MAX_RATING`
- `score_places()` — computes weighted score and returns sorted list

Scoring formula:

```
score = (DISTANCE_WEIGHT × distance_score) + (RATING_WEIGHT × rating_score)
```

---

### ✅ Phase 3 — Time Feasibility

Determines whether a place can actually be visited given the user's arrival time.

Functions added in `schedule.py`:

- `time_to_minutes()` — converts `"HH:MM"` string to minutes
- `minutes_to_time()` — converts minutes back to `"HH:MM"` string
- `estimated_travel_time()` — estimates travel time based on distance and city speed
- `is_place_open()` — checks if a place is open at a given arrival time
- `is_place_open_for_visit()` — validates that the user can arrive, enter, and complete the visit before closing time

---

### ✅ Phase 4 — Core Itinerary Engine

Builds a complete, feasible day-by-day itinerary across N days.

New file `recommendation.py`:

- `build_itinerary()` — core scheduling loop that chains visits across multiple days

Key logic implemented:

- **Distance chaining** — travel time calculated from last visited position, not user's origin
- **Wait-for-opening** — if a place opens within 30 minutes of arrival, user waits; otherwise skipped
- **End time boundary check** — places where `visit end time > DAY_END_TIME` are excluded
- **Day-end cutoff** — scheduling stops at 21:00 each day
- **Multi-day support** — unvisited places carry over to the next day; position resets to user origin each morning
