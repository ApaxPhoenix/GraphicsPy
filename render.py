import cv2
import numpy as np
from typing import List


class Render:
    def __init__(self, fps: int) -> None:
        self.fps: int = fps
        self.frames: List[np.ndarray] = []

    def animate(self) -> None:
        for frame in self.frames:
            cv2.imshow('Animation', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(np.int8(np.divide(1000, self.fps))) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()