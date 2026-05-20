import cv2
from config import LANES, MIN_VEHICLE_AREA

# Background subtractor with reduced memory footprint
bg = cv2.createBackgroundSubtractorMOG2(
    detectShadows=False,  # Disable shadow detection to save memory
    varThreshold=16      # Lower threshold to reduce history buffer size
)

def detect_vehicles_per_lane(frame):
    lane_counts = [0] * len(LANES)
    vehicles = []

    fgmask = bg.apply(frame)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        if cv2.contourArea(cnt) < MIN_VEHICLE_AREA:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2

        lane_idx = None
        for i, (lx, ly, lw, lh) in enumerate(LANES):
            if lx < cx < lx + lw and ly < cy < ly + lh:
                lane_counts[i] += 1
                lane_idx = i
                break

        vehicles.append((x, y, w, h, lane_idx))

    return lane_counts, vehicles
