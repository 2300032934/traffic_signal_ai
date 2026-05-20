import cv2

def count_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)

    # 🔴 ADD THIS PART
    if not cap.isOpened():
        print("ERROR: Video not found or cannot be opened")
        return [0, 0, 0, 0]

    lane_counts = [0, 0, 0, 0]  # 4 lanes (temporary)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # FOR NOW: just placeholder logic
        lane_counts[0] += 1

    cap.release()
    return lane_counts
