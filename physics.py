import numpy as np

class Physics:
    @staticmethod
    def linear(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Linear interpolation."""
        return np.add(start, np.multiply(progress, np.subtract(end, start)))

    @staticmethod
    def ease_in(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Ease-in interpolation."""
        progress = progress * progress
        return np.add(start, np.multiply(progress, np.subtract(end, start)))

    @staticmethod
    def ease_out(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Ease-out interpolation."""
        progress = 1 - (1 - progress) * (1 - progress)
        return np.add(start, np.multiply(progress, np.subtract(end, start)))

    @staticmethod
    def ease_in_out(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Ease-in-out interpolation."""
        progress = np.where(
            progress < 0.5,
            2 * progress * progress,
            1 - 2 * (1 - progress) * (1 - progress)
        )
        return np.add(start, np.multiply(progress, np.subtract(end, start)))
