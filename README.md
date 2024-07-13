# GraphicsPy: Simple Graphics Animation in Python

GraphicsPy is a Python framework designed to simplify graphics animation. With an intuitive API and minimalist approach, GraphicsPy makes it easy to create and animate basic geometric shapes.

## Features

- **Minimalist Design**: Focus on creating and animating shapes without unnecessary complexity.
- **Easy-to-use API**: Intuitive functions for drawing and animating shapes.
- **Customizable Physics**: Choose from different interpolation methods for smooth animations.

## Getting Started

Follow these steps to get started with GraphicsPy:

1. **Installation**

    Install the required dependencies using the provided `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

2. **Write Your Graphics Application**

    Create a Python file (e.g., `animation.py`) and start coding:

    ```python
    from physics import Physics
    from graphics import (
        PaintGrid,
        Rectangle,
        Square,
        Triangle,
        Circle
    )

    if __name__ == "__main__":
        grid = PaintGrid(500, 500, (255, 255, 255), fps=60, duration=10)
        square = Square(50, 50, 50, (0, 0, 0), physics=Physics.linear)
        rectangle = Rectangle(150, 150, 100, 50, (0, 0, 255), physics=Physics.linear)
        triangle = Triangle(250, 250, 60, (255, 0, 0), physics=Physics.linear)
        circle = Circle(350, 350, 40, (0, 255, 0), physics=Physics.linear)
        grid.draw(square)
        grid.draw(rectangle)
        grid.draw(triangle)
        grid.draw(circle)
        square.translate(450, 450)
        rectangle.translate(300, 300)
        triangle.translate(400, 400)
        circle.translate(100, 100)
        circle.translate(200, 200)
        grid.animate()
    ```

3. **Run Your Graphics Application**

    Execute your script:

    ```bash
    python animation.py
    ```

    Watch as GraphicsPy animates your shapes!

## License

GraphicsPy is released under the CC0-1.0 License. See [LICENSE](LICENSE) for details.
