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
SUN_RADIUS = 40  # Radius of the Sun
EARTH_DISTANCE = 130  # Distance from Sun to Earth
EARTH_RADIUS = 30  # Radius of Earth
MOON_DISTANCE = 50  # Distance from Earth to Moon
MARS_DISTANCE = 230  # Distance from Sun to Mars

# Orbital parameters for asteroids
APOLLO_SEMI_MAJOR_AXIS = 300  # Apollo
APOLLO_SEMI_MINOR_AXIS = 200   # Apollo
ATEN_SEMI_MAJOR_AXIS = 160      # Aten
ATEN_SEMI_MINOR_AXIS = 130      # Aten


# Colors
SUN_COLOR = (255, 204, 0)  # Yellow for the Sun
OCEAN_COLOR = (0, 102, 204)  # Ocean blue for Earth
LAND_COLOR = (34, 139, 34)    # Forest green for land
MOON_COLOR = (200, 200, 200)  # Gray for the Moon
MARS_COLOR = (255, 0, 0)      # Red for Mars
APOLLO_COLOR = (255, 0, 0)  # Red for Apollo
ATEN_COLOR = (255, 165, 0)   # Orange for Aten


# Asteroid URLs
ASTEROID_URLS = {
    "Apollo": "https://en.wikipedia.org/wiki/Apollo_asteroid",
    "Aten": "https://en.wikipedia.org/wiki/Aten_asteroid",
    
}

# Moon URL
MOON_URL = "https://en.wikipedia.org/wiki/Moon"

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Near-Earth Asteroids with Adjusted Orbits")
clock = pygame.time.Clock()

def draw_earth(x, y):
    pygame.draw.circle(screen, OCEAN_COLOR, (int(x), int(y)), EARTH_RADIUS)
    land_positions = [
        (x + 10, y + 10), (x - 15, y - 5), (x - 5, y + 20),
        (x + 20, y - 10), (x - 10, y - 15)
    ]
    for pos in land_positions:
        pygame.draw.circle(screen, LAND_COLOR, (int(pos[0]), int(pos[1])), 8)

def draw_mars(x, y):
    pygame.draw.circle(screen, MARS_COLOR, (int(x), int(y)), 25)

def draw_orbital_paths():
    pygame.draw.circle(screen, (0, 255, 255), (CENTER_X, CENTER_Y), EARTH_DISTANCE, 1)  # Earth's orbit
    pygame.draw.circle(screen, (255, 0, 255), (CENTER_X, CENTER_Y), MARS_DISTANCE, 1)   # Mars' orbit

    # Apollo's elliptical orbit
    apollo_center_x = CENTER_X - 80
    pygame.draw.ellipse(screen, APOLLO_COLOR, 
                        (apollo_center_x - APOLLO_SEMI_MAJOR_AXIS, CENTER_Y - APOLLO_SEMI_MINOR_AXIS / 2, 
                         2 * APOLLO_SEMI_MAJOR_AXIS, APOLLO_SEMI_MINOR_AXIS), 1)  # Apollo
    
    # Aten's elliptical orbit
    pygame.draw.ellipse(screen, ATEN_COLOR, 
                        (CENTER_X - ATEN_SEMI_MAJOR_AXIS, CENTER_Y - ATEN_SEMI_MINOR_AXIS / 2, 
                         2 * ATEN_SEMI_MAJOR_AXIS, ATEN_SEMI_MINOR_AXIS), 1)  # Aten
    
  
def draw_asteroids(angle_offset):
    # Apollo asteroid
    apollo_angle = angle_offset * 0.5
    apollo_x = CENTER_X - 80 + APOLLO_SEMI_MAJOR_AXIS * np.cos(apollo_angle)
    apollo_y = CENTER_Y + (APOLLO_SEMI_MINOR_AXIS / 2) * np.sin(apollo_angle)
    pygame.draw.circle(screen, APOLLO_COLOR, (int(apollo_x), int(apollo_y)), 5)  # Apollo

    # Aten asteroid
    aten_angle = angle_offset * 0.7
    aten_x = CENTER_X + ATEN_SEMI_MAJOR_AXIS * np.cos(aten_angle)
    aten_y = CENTER_Y + (ATEN_SEMI_MINOR_AXIS / 2) * np.sin(aten_angle)
    pygame.draw.circle(screen, ATEN_COLOR, (int(aten_x), int(aten_y)), 5)  # Aten

   

    return (apollo_x, apollo_y), (aten_x, aten_y), 
def draw_table():
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("Asteroids: Apollo, Aten, Amor (Click to learn more)", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def draw_example_text():
    font = pygame.font.SysFont("Arial", 10)
    example_text = font.render("**The orbits of Apollo and Aten are examples.Example for apollo asteroid is 2024 TL2 which will aproach earth on 6th october 2024 at a distance of 1,06,000km ", True, (255, 255, 255))
    screen.blit(example_text, (WIDTH // 2 - 350, HEIGHT - 50))  # Centered at bottom

async def main():
    time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = np.array(event.pos)
                apollo_pos, aten_pos, amor_pos = draw_asteroids(time * 0.05)

                # Check if Apollo asteroid was clicked
                if np.linalg.norm(mouse_pos - np.array(apollo_pos)) < 5:
                    webbrowser.open(ASTEROID_URLS["Apollo"])

                # Check if Aten asteroid was clicked
                if np.linalg.norm(mouse_pos - np.array(aten_pos)) < 5:
                    webbrowser.open(ASTEROID_URLS["Aten"])

              

                # Check if Moon was clicked
                moon_x = earth_x + MOON_DISTANCE * np.cos(time * 2 * np.pi / 40)
                moon_y = earth_y + MOON_DISTANCE * np.sin(time * 2 * np.pi / 40)
                if np.linalg.norm(mouse_pos - np.array((moon_x, moon_y))) < 10:
                    webbrowser.open(MOON_URL)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the Sun
        pygame.draw.circle(screen, SUN_COLOR, (CENTER_X, CENTER_Y), SUN_RADIUS)

        # Calculate Earth's position
        earth_angle = time * 2 * np.pi / 365
        earth_x = CENTER_X + EARTH_DISTANCE * np.cos(earth_angle)
        earth_y = CENTER_Y + EARTH_DISTANCE * np.sin(earth_angle)

        # Draw Earth
        draw_earth(earth_x, earth_y)

        # Calculate Moon's position
        moon_angle = time * 2 * np.pi / 40
        moon_x = earth_x + MOON_DISTANCE * np.cos(moon_angle)
        moon_y = earth_y + MOON_DISTANCE * np.sin(moon_angle)
        
        # Draw Moon
        pygame.draw.circle(screen, MOON_COLOR, (int(moon_x), int(moon_y)), 10)

        # Calculate Mars' position
        mars_angle = time * 2 * np.pi / 687  # Mars orbits the Sun every 687 frames
        mars_x = CENTER_X + MARS_DISTANCE * np.cos(mars_angle)
        mars_y = CENTER_Y + MARS_DISTANCE * np.sin(mars_angle)

        # Draw Mars
        draw_mars(mars_x, mars_y)

        # Draw orbital paths
        draw_orbital_paths()

        # Draw Near-Earth Asteroids and get their positions
        draw_asteroids(time)

        # Draw table for asteroids
        draw_table()

        # Draw example text
        draw_example_text()

        # Update display
        pygame.display.flip()
        time += 1 / FPS
        clock.tick(FPS)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
