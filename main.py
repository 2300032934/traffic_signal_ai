import cv2
from config import VIDEO_PATH, LANES
from vehicle_detection import detect_vehicles_per_lane
from signal_logic import calculate_signal_timings
from emergency_vehicle import detect_emergency_vehicles

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Cannot open video")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize frame to reduce memory usage (BEFORE processing)
    frame = cv2.resize(frame, (640, 360))  # Half size to reduce memory by 75%

    lane_counts, vehicles = detect_vehicles_per_lane(frame)

    # Detect emergency vehicles and adjust timings if needed
    emergency_lanes, emergency_flags = detect_emergency_vehicles(frame, vehicles)
    timings = calculate_signal_timings(lane_counts, emergency_lanes)

    # Add legend at the top
    cv2.putText(frame, "BLUE=Emergency | GREEN=Big Vehicle | RED=Regular Vehicle", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Draw lanes
    for i, (x, y, w, h) in enumerate(LANES):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (200, 200, 200), 1)
        label = f"Lane {i+1}: {lane_counts[i]} vehicles | {timings[i]}s"
        cv2.putText(
            frame,
            label,
            (x + 10, y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

    # Draw vehicle boxes with color coding:
    # Blue = Emergency vehicles, Green = Big vehicles, Red = Regular vehicles
    for idx, (x, y, w, h, lane_idx) in enumerate(vehicles):
        vehicle_area = w * h
        
        if emergency_flags and emergency_flags[idx]:
            # Emergency vehicle - Blue
            box_color = (255, 0, 0)
            label = "EMERGENCY"
        elif vehicle_area > 5000:
            # Big vehicle - Green
            box_color = (0, 255, 0)
            label = "BIG VEHICLE"
        else:
            # Regular/small vehicle - Red
            box_color = (0, 0, 255)
            label = "REGULAR"
        
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
        
        # Draw label above the box
        cv2.putText(
            frame,
            label,
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            box_color,
            2
        )

    cv2.imshow("AI Traffic Signal System (Live Video)", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
