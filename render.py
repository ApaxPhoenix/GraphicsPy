import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List


class Render:
    def __init__(self, fps: int) -> None:
        """Initialize Sequencer object."""
        self.fps: int = fps
        self.frames: List[np.ndarray] = []

    def animate(self) -> None:
        """Animate frames using matplotlib."""
        figure = plt.figure()
        plt.axis('off')
        images = [[plt.imshow(frame, animated=True)] for frame in self.frames]
        _ = animation.ArtistAnimation(figure, images, interval=np.divide(1000, self.fps), blit=True)
        plt.show()
