# camera/capture.py
import cv2
import numpy as np

class CameraFeed:
    def __init__(self, index=0, width=640, height=480):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release(self):
        self.cap.release()

def draw_grid(frame, size=3, start_x=200, start_y=120, cell_size=80):
    """Overlays a grid on the frame for face alignment."""
    img = frame.copy()
    for i in range(size + 1):
        # Horizontal lines
        cv2.line(img, (start_x, start_y + i * cell_size), 
                 (start_x + size * cell_size, start_y + i * cell_size), 
                 (0, 255, 0), 2)
        # Vertical lines
        cv2.line(img, (start_x + i * cell_size, start_y), 
                 (start_x + i * cell_size, start_y + size * cell_size), 
                 (0, 255, 0), 2)
    return img
