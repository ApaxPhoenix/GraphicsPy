import numpy as np


class Physics:
    @staticmethod
    def linear(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Linear interpolation."""
        return np.round(np.add(start, np.multiply(progress, np.subtract(end, start)))).astype(np.int32)

    @staticmethod
    def ease_in(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Ease-in interpolation."""
        progress = np.multiply(progress, progress)
        return np.round(np.add(start, np.multiply(progress, np.subtract(end, start)))).astype(np.int32)

    @staticmethod
    def ease_out(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Ease-out interpolation."""
        progress = np.subtract(1, np.multiply(np.subtract(1, progress), np.subtract(1, progress)))
        return np.round(np.add(start, np.multiply(progress, np.subtract(end, start)))).astype(np.int32)

    @staticmethod
    def ease_in_out(start: np.ndarray, end: np.ndarray, progress: float) -> np.ndarray:
        """Ease-in-out interpolation."""
        progress = np.where(
            np.less(progress, 0.5),
            np.multiply(2, np.multiply(progress, progress)),
            np.subtract(1, np.multiply(2, np.multiply(np.subtract(1, progress), np.subtract(1, progress))))
        )
        return np.round(np.add(start, np.multiply(progress, np.subtract(end, start)))).astype(np.int32)