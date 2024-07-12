import numpy as np
from typing import Union, Callable, List, Tuple
from PIL import Image, ImageDraw
from physics import Physics
from render import Render


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
        self.target_x: np.ndarray = np.array([x, y], dtype=np.float32)
        self.angle: np.float32 = np.float32(angle)
        self.target_angle: np.float32 = np.mod(np.add(np.float32(angle), 360), 360)
        self.size: Union[int, np.ndarray] = size
        self.color: Tuple[int, int, int] = tuple(color)
        self.radius: int = radius
        self.zindex: int = zindex
        self.physics: Callable = physics
        self.current_step: int = 0

    def translate(self, new_x: int, new_y: int) -> None:
        """Translate to new position."""
        self.target_x = np.array([new_x, new_y], dtype=np.float32)
        self.current_step = 0

    def rotate(self, angle: int) -> None:
        """Rotate to new angle."""
        self.target_angle = np.mod(np.add(self.angle, np.float32(angle)), 360)
        self.current_step = 0

    def update(self, progress: float) -> None:
        """Update position and angle based on progress."""
        self.x = self.physics(self.x, self.target_x, progress)
        self.angle = np.mod(self.physics(np.array([self.angle]), np.array([self.target_angle]), progress)[0], 360)

    def draw(self, drawer: ImageDraw.ImageDraw) -> None:
        """Draw method to be overridden in subclasses."""
        ...


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
        half_size: np.ndarray = np.divide(self.size, 2).astype(np.int32)
        top_left: np.ndarray = np.subtract(self.x, half_size)
        bottom_right: np.ndarray = np.add(self.x, half_size)
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
        half_size: np.ndarray = np.divide(self.size, 2).astype(np.int32)
        top_left: np.ndarray = np.subtract(self.x, half_size)
        bottom_right: np.ndarray = np.add(self.x, half_size)
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
        half_size: np.ndarray = np.divide(self.size, 2).astype(np.int32)
        top_point: np.ndarray = np.add(self.x, [0, -half_size])
        left_point: np.ndarray = np.add(self.x, [-half_size, half_size])
        right_point: np.ndarray = np.add(self.x, [half_size, half_size])
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
        top_left: np.ndarray = np.subtract(self.x, self.radius).astype(np.int32)
        bottom_right: np.ndarray = np.add(self.x, self.radius).astype(np.int32)
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