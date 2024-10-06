import asyncio
import pygame
import numpy as np
import sys
import webbrowser

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
SUN_RADIUS = 30  # Radius of the sun

# Planet properties (name, color, distance from the sun, orbital speed, size ratio, url)
PLANETS = [
    {"name": "Mercury", "color": (169, 169, 169), "distance": 50, "speed": 4.74 / 60, "size": 3, "url": "https://en.wikipedia.org/wiki/Mercury_(planet)"},
    {"name": "Venus", "color": (255, 204, 0), "distance": 80, "speed": 3.50 / 60, "size": 6, "url": "https://en.wikipedia.org/wiki/Venus"},
    {"name": "Earth", "color": (0, 0, 255), "distance": 110, "speed": 2.98 / 60, "size": 6, "url": "https://en.wikipedia.org/wiki/Earth"},
    {"name": "Mars", "color": (255, 0, 0), "distance": 140, "speed": 2.41 / 60, "size": 4, "url": "https://en.wikipedia.org/wiki/Mars"},
    {"name": "Jupiter", "color": (255, 165, 0), "distance": 170, "speed": 1.31 / 60, "size": 14, "url": "https://en.wikipedia.org/wiki/Jupiter"},
    {"name": "Saturn", "color": (255, 255, 0), "distance": 200, "speed": 0.97 / 60, "size": 12, "url": "https://en.wikipedia.org/wiki/Saturn"},
    {"name": "Uranus", "color": (0, 255, 255), "distance": 230, "speed": 0.68 / 60, "size": 5, "url": "https://en.wikipedia.org/wiki/Uranus"},
    {"name": "Neptune", "color": (0, 0, 139), "distance": 260, "speed": 0.54 / 60, "size": 5, "url": "https://en.wikipedia.org/wiki/Neptune"}
]

# Sun properties
SUN_URL = "https://en.wikipedia.org/wiki/Sun"

# Asteroid belt properties
ASTEROID_COUNT = 100
ASTEROID_COLOR = (169, 169, 169)
ASTEROID_SIZE = 2
ASTEROID_BELT_START = 145  # Just outside Mars
ASTEROID_BELT_END = 165    # Just inside Jupiter

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Solar System Orrery")
clock = pygame.time.Clock()

# Main function
async  def main():

    time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = np.array(event.pos)

                    # Check if sun was clicked
                    if np.linalg.norm(mouse_pos - np.array([CENTER_X, CENTER_Y])) <= SUN_RADIUS:
                        webbrowser.open(SUN_URL)

                    # Check if any planet was clicked
                    for planet in PLANETS:
                        angle = time * planet["speed"]
                        x = CENTER_X + planet["distance"] * np.cos(angle)
                        y = CENTER_Y + planet["distance"] * np.sin(angle)

                        # Check if mouse position is within the planet's bounds
                        if np.linalg.norm(mouse_pos - np.array([x, y])) <= planet["size"]:
                            webbrowser.open(planet["url"])

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw stars
        for _ in range(100):
            star_x = np.random.randint(0, WIDTH)
            star_y = np.random.randint(0, HEIGHT)
            screen.set_at((star_x, star_y), (255, 255, 255))

        # Draw the sun
        pygame.draw.circle(screen, (255, 255, 0), (CENTER_X, CENTER_Y), SUN_RADIUS)

        # Draw the sun label
        font = pygame.font.SysFont("Arial", 18)
        sun_label = font.render("Sun", True, (255, 255, 255))
        screen.blit(sun_label, (CENTER_X + 10, CENTER_Y - 10))  # Position the label next to the sun

        # Update and draw planets and their orbits
        for planet in PLANETS:
            # Calculate the angle based on time and speed
            angle = time * planet["speed"]
            x = CENTER_X + planet["distance"] * np.cos(angle)
            y = CENTER_Y + planet["distance"] * np.sin(angle)

            # Simulate 3D effect by scaling based on distance
            scale_factor = 1 / (1 + (planet["distance"] - SUN_RADIUS) / 400)  # Adjust the denominator to control scaling
            scaled_size = max(1, int(planet["size"] * scale_factor))  # Ensure size is at least 1

            # Draw the orbit
            pygame.draw.circle(screen, (100, 100, 100), (CENTER_X, CENTER_Y), int(planet["distance"]), 1)

            # Draw the planet
            pygame.draw.circle(screen, planet["color"], (int(x), int(y)), scaled_size)

            # Draw the planet label
            label = font.render(planet["name"], True, (255, 255, 255))
            screen.blit(label, (int(x) + 10, int(y) - 10))  # Adjust position to avoid overlap

            # Draw Saturn's rings
            if planet["name"] == "Saturn":
                # Draw an ellipse for the rings
                pygame.draw.ellipse(screen, (200, 200, 200), (int(x) - 20, int(y) - 5, 40, 10), 2)

        # Draw the asteroid belt
        for _ in range(ASTEROID_COUNT):
            # Random angle and distance within the asteroid belt range
            angle = np.random.uniform(0, 2 * np.pi)
            distance = np.random.uniform(ASTEROID_BELT_START, ASTEROID_BELT_END)
            asteroid_x = CENTER_X + distance * np.cos(angle)
            asteroid_y = CENTER_Y + distance * np.sin(angle)
            pygame.draw.circle(screen, ASTEROID_COLOR, (int(asteroid_x), int(asteroid_y)), ASTEROID_SIZE)

        # Update display
        pygame.display.flip()
        time += 1 / FPS
        clock.tick(FPS)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
