**Phase 3 — Time Feasibility**

Added time feasibility checks to determine whether a place can actually be visited given the user's arrival time.

Functions added in `schedule.py`:

- `time_to_minutes()` — converts "HH:MM" string to minutes
- `estimated_travel_time()` — estimates travel time based on distance and city speed
- `is_place_open()` — checks if a place is open at a given time
- `is_place_open_for_visit()` — validates that the user can arrive, enter, and complete the visit before closing time
