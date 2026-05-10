# detection/color_detection.py
import cv2
import numpy as np
from utils.colors import get_color_name

def extract_colors_from_frame(frame, size=3, start_x=200, start_y=120, cell_size=80):
    """
    Extracts average color from each cell in the grid.
    frame is expected to be in RGB.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    colors = []
    
    offset = int(cell_size * 0.2)
    
    for row in range(size):
        for col in range(size):
            cx = start_x + col * cell_size + cell_size // 2
            cy = start_y + row * cell_size + cell_size // 2
            
            # Sample a small region in the center of the cell
            # Clamp bounds to avoid out-of-frame slicing (which returns empty arrays)
            y1 = max(0, cy - offset)
            y2 = min(hsv_frame.shape[0], cy + offset)
            x1 = max(0, cx - offset)
            x2 = min(hsv_frame.shape[1], cx + offset)
            roi = hsv_frame[y1:y2, x1:x2]
            
            if roi.size == 0:
                colors.append('UNKNOWN')
                continue
            
            avg_color = np.median(roi, axis=(0, 1))
            color_name = get_color_name(avg_color)
            colors.append(color_name)
            
    return colors
