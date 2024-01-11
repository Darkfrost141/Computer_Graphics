import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Constants
WIDTH = 700  # Increase the window width
HEIGHT = 700  # Increase the window height
COLOR_RED = (1, 0, 0)
COLOR_BLUE = (0, 0, 1)
COLOR_GREEN = (0, 1, 0)
COLOR_WHITE = (1, 1, 1)
COLOR_BLACK = (0, 0, 0)

is_raining = True
wind_speed = 5
rain_speed = 500
is_daylight = True  # Start with daylight

# Define the house
def draw_house():
    # Roof (Red Color)
    glColor3fv(COLOR_RED)  # Set color to red
    glBegin(GL_TRIANGLES)
    glVertex2f(180, 480)  # Bottom-left corner
    glVertex2f(385, 600)  # Top corner
    glVertex2f(590, 480)  # Bottom-right corner
    glEnd()
    # Base
    glColor3fv(COLOR_BLUE)  # Set color to blue
    glBegin(GL_QUADS)
    glVertex2f(180, 300)  # Top-left corner
    glVertex2f(590, 300)  # Top-right corner
    glVertex2f(590, 480)  # Bottom-right corner
    glVertex2f(180, 480)  # Bottom-left corner
    glEnd()

    # Calculate the door center
    door_center_x = 370

    # Door
    glColor3fv(COLOR_RED)  # Set color to red
    glBegin(GL_QUADS)
    door_width = 80
    door_height = 150
    glVertex2f(door_center_x - door_width / 2, 300)  # Top-left corner
    glVertex2f(door_center_x + door_width / 2, 300)  # Top-right corner
    glVertex2f(door_center_x + door_width / 2, 300 + door_height)  # Bottom-right corner
    glVertex2f(door_center_x - door_width / 2, 300 + door_height)  # Bottom-left corner
    glEnd()

    # Windows
    glColor3fv(COLOR_GREEN)  # Set color to green
    glBegin(GL_QUADS)
    glVertex2f(220, 360)  # Bottom-left corner
    glVertex2f(260, 360)  # Bottom-right corner
    glVertex2f(260, 400)  # Top-right corner
    glVertex2f(220, 400)  # Top-left corner
    glEnd()


def change_option():
    global wind_speed, rain_speed, is_raining, is_daylight
    straight_rain = False

    for event in pygame.event.get():
        if event.type == QUIT:
            is_raining = False
        if event.type == KEYDOWN:
            if event.key == K_d:
                wind_speed = -5
            elif event.key == K_a:
                wind_speed = 5
            elif event.key == K_w:
                if rain_speed > 100:
                    rain_speed -= 200
            elif event.key == K_s:
                straight_rain = not straight_rain
            elif event.key == K_SPACE:
                is_daylight = not is_daylight
                if not is_daylight:
                    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
                else:
                    glClearColor(1.0, 1.0, 1.0, 1.0)  # Set background color to white

    if straight_rain:
        wind_speed = 0

def draw_rain():
    for _ in range(1000):  # Increase the number of raindrops

        # Randomize x and y coordinates for a wider distribution
        x = random.randint(0, WIDTH)
        y = random.randint(300, HEIGHT)

        if wind_speed != 0:
            glVertex2f(x, y)
            glVertex2f(x + wind_speed, y + 5)
        else:
            glVertex2f(x, y)
            glVertex2f(x, y + 5)


def main():
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)

    while is_raining:
        change_option()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_house()

        if not is_daylight:
            glColor3fv(COLOR_WHITE)
            glBegin(GL_LINES)
            draw_rain()
            glEnd()

        pygame.display.flip()
        pygame.time.delay(rain_speed)

if __name__ == "__main__":
    main()

