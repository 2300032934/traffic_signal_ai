import cv2
from config import LANES

def draw_lanes_and_signals(frame, lane_counts, timings):
    for i, (x, y, w, h) in enumerate(LANES):
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(
            frame,
            f"Lane {i+1}: {lane_counts[i]} | {timings[i]}s",
            (x+10, y+40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )
    return frame
