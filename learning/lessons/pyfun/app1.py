import base64
import math
import random
import turtle
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pygame
from matplotlib.animation import FuncAnimation

# Set up the environment
plt.rcParams["figure.figsize"] = (6, 4)
plt.rcParams["figure.facecolor"] = "#f0f0f0"

# Create a simple interactive menu
print("Welcome to the Advanced Python Playground!")
print("Available demonstrations:")
print("1. PyGame Visualizations")
print("2. Mathematical Animations")
print("3. Turtle G***hics Art")
print("4. Data Visualization")
print("5. Interactive Physics Simulation")


def run_pygame_demo():
    """Run a simple PyGame visualization"""
    try:
        # Initialize Pygame
        pygame.init()

        # Set up the window
        width, height = 600, 400
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Particle Simulation")

        # Create particles
        particles = []
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            speed_x = random.uniform(-1, 1)
            speed_y = random.uniform(-1, 1)
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255),
            )
            size = random.randint(2, 8)
            particles.append([x, y, speed_x, speed_y, color, size])

        # Main loop
        running = True
        clock = pygame.time.Clock()
        while running and len(particles) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with a semi-transparent black to create trails
            screen.fill((0, 0, 0, 10))

            # Update and draw particles
            for p in particles:
                p[0] += p[2]  # x position
                p[1] += p[3]  # y position

                # Bounce off walls
                if p[0] <= 0 or p[0] >= width:
                    p[2] *= -1
                if p[1] <= 0 or p[1] >= height:
                    p[3] *= -1

                # Draw the particle
                pygame.draw.circle(screen, p[4], (int(p[0]), int(p[1])), p[5])

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return "PyGame demo completed!"
    except Exception as e:
        return f"PyGame error: {e}"


def run_animation_demo():
    """Create a mathematical animation"""
    try:
        # Create a figure and axis
        fig, ax = plt.subplots()
        x = np.linspace(0, 2 * np.pi, 200)
        (line,) = ax.plot(x, np.sin(x))
        ax.set_ylim(-1.5, 1.5)

        # Animation update function
        def update(frame):
            line.set_ydata(np.sin(x + frame / 10))
            return (line,)

        # Create animation
        ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)

        # Save as HTML video
        video = ani.to_jshtml()
        plt.close(fig)
        return video
    except Exception as e:
        return f"Animation error: {e}"


def run_turtle_demo():
    """Create turtle g***hics art"""
    try:
        # Set up turtle
        t = turtle.Turtle()
        t.speed(0)
        turtle.bgcolor("black")
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]

        # Draw a colorful spiral
        for i in range(180):
            t.color(colors[i % 6])
            t.forward(i * 2)
            t.right(59)

        # Get the drawing as an image
        canvas = turtle.getcanvas()
        ps = canvas.postscript(colormode="color")
        img = BytesIO()
        img.write(ps.encode("utf-8"))
        img_data = base64.b64encode(img.getvalue()).decode("utf-8")
        turtle.bye()

        return f'<img src="data:image/postscript;base64,{img_data}" width="400" height="400">'
    except Exception as e:
        return f"Turtle error: {e}"


def run_data_viz_demo():
    """Create an interesting data visualization"""
    try:
        # Generate some data
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.sin(x) * np.cos(x)

        # Create the plot
        fig, ax = plt.subplots()
        ax.plot(x, y1, label="sin(x)")
        ax.plot(x, y2, label="cos(x)")
        ax.plot(x, y3, label="sin(x)*cos(x)")
        ax.legend()
        ax.set_title("Trigonometric Functions")
        ax.grid(True)

        # Convert to HTML
        img = BytesIO()
        plt.savefig(img, format="png")
        img_data = base64.b64encode(img.getvalue()).decode("utf-8")
        plt.close(fig)

        return f'<img src="data:image/png;base64,{img_data}" width="600" height="400">'
    except Exception as e:
        return f"Data visualization error: {e}"


def run_physics_demo():
    """Run a simple physics simulation"""
    try:
        # Simple gravity simulation
        fig, ax = plt.subplots()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        # Initial conditions
        g = 9.8  # gravity
        v0 = 15  # initial velocity
        angle = 45  # degrees
        theta = np.radians(angle)
        t_flight = 2 * v0 * np.sin(theta) / g
        t = np.linspace(0, t_flight, 100)

        # Calculate trajectory
        x = v0 * np.cos(theta) * t
        y = v0 * np.sin(theta) * t - 0.5 * g * t**2

        # Create the plot
        (line,) = ax.plot(x, y, "r-")
        (point,) = ax.plot([x[0]], [y[0]], "ro")
        ax.set_title("Projectile Motion Simulation")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Height (m)")
        ax.grid(True)

        # Animation function
        def update(frame):
            point.set_data([x[frame]], [y[frame]])
            return (point,)

        # Create animation
        ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

        # Save as HTML video
        video = ani.to_jshtml()
        plt.close(fig)
        return video
    except Exception as e:
        return f"Physics simulation error: {e}"


# Run the selected demo based on user input
def main():
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        result = run_pygame_demo()
    elif choice == "2":
        result = run_animation_demo()
    elif choice == "3":
        result = run_turtle_demo()
    elif choice == "4":
        result = run_data_viz_demo()
    elif choice == "5":
        result = run_physics_demo()
    else:
        result = "Invalid choice. Please run again and select 1-5."

    print(result)


if __name__ == "__main__":
    main()
