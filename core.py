import numpy as np
from typing import Union, Callable, List, Tuple
from PIL import Image, ImageDraw
from .physics import Physics
from .render import Render


class RootPart:
    def __init__(
            self,
            x: int,
            y: int,
            size: Union[int, list],
            color: Tuple[int, int, int] = (0, 0, 0),
            angle: int = 0,
            radius: int = 0,
            zindex: int = 0,
            physics: Callable = Physics.linear
    ) -> None:
        """Initialize RootPart object."""
        self.x: np.ndarray = np.array([x, y], dtype=np.float32)
        self.targets: List[np.ndarray] = [np.array([x, y], dtype=np.float32)]
        self.angle: np.float32 = np.float32(angle)
        self.target_angle: np.float32 = np.mod(np.add(np.float32(angle), 360), 360)
        self.size: Union[int, np.ndarray] = size
        self.color: Tuple[int, int, int] = tuple(color)
        self.radius: int = radius
        self.zindex: int = zindex
        self.physics: Callable = physics
        self.current_step: int = 0
        self.translation_progress: float = 0.0
        self.wait_steps: int = 0
        self.removed: bool = False

    def translate(self, new_positions: List[int]) -> None:
        """Translate to new positions sequentially."""
        new_targets = [np.array(new_positions[i:i + 2], dtype=np.float32) for i in range(0, len(new_positions), 2)]
        self.targets.extend(new_targets)
        self.current_step = 0
        self.translation_progress = 0.0

    def rotate(self, angle: int) -> None:
        """Rotate to new angle."""
        self.target_angle = np.mod(np.add(self.angle, np.float32(angle)), 360)
        self.current_step = 0

    def wait(self, steps: int) -> None:
        """Wait for a specified number of steps."""
        self.wait_steps = steps

    def update(self, progress: float) -> None:
        """Update position and angle based on progress."""
        if self.wait_steps > 0:
            self.wait_steps -= 1
            return

        if self.targets:
            self.translation_progress = np.add(self.translation_progress, progress)
            self.x = self.physics(self.x, self.targets[0], self.translation_progress)
            if np.allclose(self.x, self.targets[0], atol=1.0):
                self.targets.pop(0)
                self.translation_progress = 0.0  # Reset progress for the next target
        self.angle = np.mod(self.physics(np.array([self.angle]), np.array([self.target_angle]), progress)[0], 360)

    def remove(self) -> None:
        """Remove the object from memory."""
        if not self.removed:
            for attr in list(self.__dict__.keys()):
                if attr != 'removed':
                    delattr(self, attr)
            self.removed = True
            print(f"Object of type {self.__class__.__name__} has been removed from memory.")
        else:
            print(f"Object of type {self.__class__.__name__} has already been removed.")

    def draw(self, drawer: ImageDraw.ImageDraw) -> None:
        """Draw method to be overridden in subclasses."""
        pass


class Square(RootPart):
    def __init__(
            self,
            x: int,
            y: int,
            size: int,
            color: Tuple[int, int, int] = (0, 0, 0),
            zindex: int = 0,
            physics: Callable = Physics.linear
    ) -> None:
        """Initialize SquarePart object."""
        super().__init__(x, y, size, color, zindex=zindex, physics=physics)

    def draw(self, drawer: ImageDraw.ImageDraw) -> None:
        """Draw square on ImageDraw object."""
        half_size = np.divide(self.size, 2).astype(np.int32)
        top_left = np.subtract(self.x, half_size).astype(np.int32)
        bottom_right = np.add(self.x, half_size).astype(np.int32)
        drawer.rectangle([tuple(top_left), tuple(bottom_right)], fill=self.color)


class Rectangle(RootPart):
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            color: Tuple[int, int, int] = (0, 0, 0),
            zindex: int = 0,
            physics: Callable = Physics.linear
    ) -> None:
        """Initialize RectanglePart object."""
        size = [width, height]
        super().__init__(x, y, size, color, zindex=zindex, physics=physics)

    def draw(self, drawer: ImageDraw.ImageDraw) -> None:
        """Draw rectangle on ImageDraw object."""
        half_size = np.divide(self.size, 2).astype(np.int32)
        top_left = np.subtract(self.x, half_size).astype(np.int32)
        bottom_right = np.add(self.x, half_size).astype(np.int32)
        drawer.rectangle([tuple(top_left), tuple(bottom_right)], fill=self.color)


class Triangle(RootPart):
    def __init__(
            self,
            x: int,
            y: int,
            size: int,
            color: Tuple[int, int, int] = (0, 0, 0),
            zindex: int = 0,
            physics: Callable = Physics.linear
    ) -> None:
        """Initialize TrianglePart object."""
        super().__init__(x, y, size, color, zindex=zindex, physics=physics)

    def draw(self, drawer: ImageDraw.ImageDraw) -> None:
        """Draw triangle on ImageDraw object."""
        half_size = np.divide(self.size, 2).astype(np.int32)
        top_point = np.add(self.x, [0, -half_size])
        left_point = np.add(self.x, [-half_size, half_size])
        right_point = np.add(self.x, [half_size, half_size])
        drawer.polygon([tuple(top_point), tuple(left_point), tuple(right_point)], fill=self.color)


class Circle(RootPart):
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            color: Tuple[int, int, int] = (0, 0, 0),
            zindex: int = 0,
            physics: Callable = Physics.linear
    ) -> None:
        """Initialize CirclePart object."""
        super().__init__(x, y, radius * 2, color, radius=radius, zindex=zindex, physics=physics)

    def draw(self, drawer: ImageDraw.ImageDraw) -> None:
        """Draw circle on ImageDraw object."""
        top_left = np.subtract(self.x, self.radius).astype(np.int32)
        bottom_right = np.add(self.x, self.radius).astype(np.int32)
        drawer.ellipse([tuple(top_left), tuple(bottom_right)], fill=self.color)


class PaintGrid:
    def __init__(
            self,
            width: int,
            height: int,
            background_color: Tuple[int, int, int] = (255, 255, 255),
            fps: int = 30,
            duration: int = 1
    ) -> None:
        """Initialize PaintGrid object."""
        self.width: int = width
        self.height: int = height
        self.fps: int = fps
        self.duration: int = duration
        self.background_color: Tuple[int, int, int] = tuple(background_color)
        self.steps: int = np.multiply(fps, duration)
        self.figures: List[RootPart] = []

    def draw(self, figure: 'RootPart') -> None:
        """Add figure to PaintGrid."""
        if not isinstance(figure, RootPart):
            raise ValueError("Invalid figure. Must be a RootPart object.")
        self.figures.append(figure)

    def animate(self) -> None:
        """Animate figures in PaintGrid."""
        render = Render(self.fps)
        for frame in np.arange(self.steps):
            image = Image.new("RGB", (self.width, self.height), self.background_color)
            drawer = ImageDraw.Draw(image)
            progress = np.divide(frame, self.steps)
            for shape in self.figures:
                shape.update(progress)
                shape.draw(drawer)
            render.frames.append(np.array(image))
        render.animate()
