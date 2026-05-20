def calculate_signal_timings(lane_counts, emergency_lanes=None):
    """Calculate signal timings per lane.

    If `emergency_lanes` is provided and any lane has an emergency vehicle,
    give priority to those lanes (long green), and shorten others.
    """
    timings = []

    # If emergency present, prioritize emergency lanes
    if emergency_lanes and any(emergency_lanes):
        for i, _ in enumerate(lane_counts):
            if emergency_lanes[i]:
                timings.append(90)
            else:
                timings.append(10)
        return timings

    for count in lane_counts:
        if count > 20:
            timings.append(60)
        elif count > 10:
            timings.append(40)
        else:
            timings.append(20)

    return timings
