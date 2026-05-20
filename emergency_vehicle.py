import cv2
import numpy as np
from config import LANES

def detect_emergency_vehicles(frame, vehicles, lanes=LANES):
    """Detect emergency vehicles within detected vehicle bounding boxes.

    Simple heuristic: look for bright red or blue light patches (siren lights)
    within each vehicle bounding box. Returns two values:
      * emergency_per_lane: list of booleans per lane indicating whether an
        emergency vehicle is present in that lane (used for timing logic).
      * emergency_flags: list of booleans parallel to ``vehicles`` signaling
        which individual detections are classified as emergency. This allows
        the visualization layer to color those boxes differently.
    """
    emergency_per_lane = [False] * len(lanes)
    emergency_flags = [False] * len(vehicles)

    for idx, (x, y, w, h, lane_idx) in enumerate(vehicles):
        if lane_idx is None:
            continue

        # Safeguard crop boundaries
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(frame.shape[1], x + w), min(frame.shape[0], y + h)
        roi = frame[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Red range (two ranges in HSV)
        lower_red1 = np.array([0, 120, 200])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 120, 200])
        upper_red2 = np.array([180, 255, 255])

        # Blue range
        lower_blue = np.array([90, 120, 150])
        upper_blue = np.array([140, 255, 255])

        mask_r1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_r2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_b = cv2.inRange(hsv, lower_blue, upper_blue)

        mask = cv2.bitwise_or(mask_r1, mask_r2)
        mask = cv2.bitwise_or(mask, mask_b)

        # If bright colored pixels cover a small portion of the bbox, flag as emergency
        nonzero = cv2.countNonZero(mask)
        area = max(1, roi.shape[0] * roi.shape[1])
        if nonzero / area > 0.01:
            emergency_flags[idx] = True
            if lane_idx is not None:
                emergency_per_lane[lane_idx] = True

    return emergency_per_lane, emergency_flags
