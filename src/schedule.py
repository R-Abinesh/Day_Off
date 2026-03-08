import config

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return int(hours * 60 + minutes)

def minutes_to_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def estimated_travel_time(distance_km):
    return int((distance_km / config.CITY_SPEED) * 60)

def is_place_open(slot, arrival_time):
    slot_start = time_to_minutes(slot['start'])
    slot_end   = time_to_minutes(slot['end'])

    wait = slot_start - arrival_time

    # Too much waiting → skip this slot
    if wait > config.MAX_WAIT_TIME:
        return False, None

    # Effective start — either arrive or wait for opening
    effective_start = max(arrival_time, slot_start)

    if slot_start <= effective_start <= slot_end:
        return True, effective_start

    return False, None

def is_place_open_for_visit(place, arrival_time):
    for slot in place['open_hours']:
        is_open, effective_start = is_place_open(slot, arrival_time)
        if is_open:
            time_available = time_to_minutes(slot['end']) - effective_start
            if time_available >= place['visit_duration']:
                end_time = effective_start + place['visit_duration']
                return True, effective_start, end_time
    return False, None, None

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return int(hours * 60 + minutes)

def estimated_travel_time(distance_km):
    return int((distance_km / config.CITY_SPEED) * 60)

def is_place_open(slot, arrival_time):
    slot_start = time_to_minutes(slot['start'])
    slot_end   = time_to_minutes(slot['end'])

    wait = slot_start - arrival_time

    # Too much waiting → skip this slot
    if wait > config.MAX_WAIT_TIME:
        return False, None

    # Effective start — either arrive or wait for opening
    effective_start = max(arrival_time, slot_start)

    if slot_start <= effective_start <= slot_end:
        return True, effective_start

    return False, None

def is_place_open_for_visit(place, arrival_time):
    for slot in place['open_hours']:
        is_open, effective_start = is_place_open(slot, arrival_time)
        if is_open:
            time_available = time_to_minutes(slot['end']) - effective_start
            if time_available >= place['visit_duration']:
                end_time = effective_start + place['visit_duration']
                return True, effective_start, end_time
    return False, None, None