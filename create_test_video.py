import cv2
import numpy as np

# Create a test video with 4 lanes
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('sample_video.mp4', fourcc, 20.0, (1280, 720))

for frame_num in range(100):
    # Create a frame with 4 lanes
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    # Draw lane dividers
    cv2.line(frame, (320, 0), (320, 720), (255, 255, 255), 2)
    cv2.line(frame, (640, 0), (640, 720), (255, 255, 255), 2)
    cv2.line(frame, (960, 0), (960, 720), (255, 255, 255), 2)
    
    # Draw some vehicle rectangles in each lane
    for lane in range(4):
        x_offset = lane * 320
        # Add some simulated vehicles
        vehicles = 2 + (frame_num // 20) % 3
        for v in range(vehicles):
            y = 100 + v * 150
            cv2.rectangle(frame, (x_offset + 50, y), (x_offset + 270, y + 100), (0, 255, 0), -1)
    
    # Add frame number
    cv2.putText(frame, f'Frame {frame_num}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    out.write(frame)

out.release()
print('Test video created successfully!')
