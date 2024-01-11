from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin
import random

def midpointcircle(x, y, r, color):
    glColor3f(*color) # Set the color
    glBegin(GL_POINT)
    glPointSize(1)
    #N, S, E, W from center
    d = 1.25-r
    x1 = x 
    y1 = y
    x = 0 
    y = r 
    if x1 != 0 or y1!=0:
        glVertex2f(x+x1, y+y1)
        glVertex2f(y+y1, x+x1)
        glVertex2f(y+y1, -x+x1)
        glVertex2f(x+x1, -y+y1)
        glVertex2f(-x+x1, -y+y1)
        glVertex2f(-y+y1, -x+x1)
        glVertex2f(-y+y1, x+x1)
        glVertex2f(-x+x1, y+y1)
    else: 
        glVertex2f(x, y)
        glVertex2f(y, x)
        glVertex2f(y, -x)
        glVertex2f(x, -y)
        glVertex2f(-x, -y)
        glVertex2f(-y, -x)
        glVertex2f(-y, x)
        glVertex2f(-x, y)
    while x <= y:
        if d<0:
            #E
            d = d+2*x+3 
            x += 1  
        else:
            d = d + 2*x - 2*y + 5
            x = x + 1 
            y = y - 1 
        if x1 != 0 or y1!=0:
            glVertex2f(x+x1, y+y1)
            glVertex2f(y+y1, x+x1)
            glVertex2f(y+y1, -x+x1)
            glVertex2f(x+x1, -y+y1)
            glVertex2f(-x+x1, -y+y1)
            glVertex2f(-y+y1, -x+x1)
            glVertex2f(-y+y1, x+x1)
            glVertex2f(-x+x1, y+y1)
        else: 
            glVertex2f(x, y)
            glVertex2f(y, x)
            glVertex2f(y, -x)
            glVertex2f(x, -y)
            glVertex2f(-x, -y)
            glVertex2f(-y, -x)
            glVertex2f(-y, x)
            glVertex2f(-x, y)
    glEnd()

# Mid point line drawing algo
def drawPoint(x, y):
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx >= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 0
        else:
            return 1
    elif dx <= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 3
        else:
            return 2
    elif dx <= 0 and dy <= 0:
        if abs(dx) > abs(dy):
            return 4
        else:
            return 5
    else:  # dx >= 0 and dy <= 0
        if abs(dx) > abs(dy):
            return 7
        else:
            return 6

def midPointAlgo(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1, x2, y2 = convertToZoneZero(x1, y1, x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    while x <= x2:
        tx, ty = convertFromZoneZeroToZoneSmth(x, y, zone)
        drawPoint(tx, ty)  # Assuming that we have a drawPoint function for drawing the point
        x += 1
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE


def convertToZoneZero(x1, y1, x2, y2, zone):
    zone_mappings = {
        0: (x1, y1, x2, y2),
        1: (y1, x1, y2, x2),
        2: (y1, -x1, y2, -x2),
        3: (-x1, y1, -x2, y2),
        4: (-x1, -y1, -x2, -y2),
        5: (-y1, -x1, -y2, -x2),
        6: (-y1, x1, -y2, x2),
        7: (x1, -y1, x2, -y2),
    }

    return zone_mappings[zone]


def convertFromZoneZeroToZoneSmth(x, y, zone):
    zone_mappings = {
        0: (x, y),
        1: (y, x),
        2: (-y, x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (y, -x),
        7: (x, -y),
    }

    return zone_mappings[zone]


# Midpoint Circle Drawing Algorithm
def midpointcircle(x, y, r, color):
    glColor3f(*color)
    glPointSize(2)  # pixel size
    glBegin(GL_POINTS)
    d = 1.25 - r
    x1 = x
    y1 = y
    x = 0
    y = r
    while x <= y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * x - 2 * y + 5
            x += 1
            y -= 1
        # Draw horizontal lines (or points) between boundary points for all octants
        for fill_x in range(int(-x + x1), int(x + x1 + 1)):
            glVertex2f(fill_x, y + y1)
            glVertex2f(fill_x, -y + y1)
        for fill_x in range(int(-y + x1), int(y + x1 + 1)):
            glVertex2f(fill_x, x + y1)
            glVertex2f(fill_x, -x + y1)
    glEnd()


sun_scale = 1.0  # Global variable to control the scaling of the sun
def draw_circle(x_center, y_center, radius, color):
    if len(color) == 3:
        glColor3f(*color) # Set the color
    elif len(color) ==4:
        glColor4f(*color)
    glBegin(GL_POLYGON)
    num_segments = 100 # Number of segments for smooth circle
    for i in range(num_segments):
        theta = 2.0 * 3.1415926 * i / num_segments
        dx = radius * cos(theta)
        dy = radius * sin(theta)
        glVertex2f(dx + x_center, dy + y_center)
    glEnd()


def draw_circle_X(x_center, y_center, radius, color):
    if len(color) == 3:
        glColor3f(*color) # Set the color
    elif len(color) ==4:
        glColor4f(*color)
    glBegin(GL_POLYGON)
    num_segments = 100 # Number of segments for smooth circle
    for i in range(num_segments):
        theta = 2.0 * 3.1415926 * i / num_segments
        dx = radius * sun_scale * cos(theta)
        dy = radius * sun_scale * sin(theta)
        glVertex2f(dx + x_center, dy + y_center)
    glEnd()

def draw_treeX(x, y):
    glColor3f(0.5, 0.3, 0.0)
    midPointAlgo(x + 10, y + 50, x + 10, y - 70)
    midPointAlgo(x - 10, y + 50, x - 10, y - 70)
    midPointAlgo(x + 10, y - 70, x - 10, y - 70)
    tree_leaf(x, y + 50)


def tree_leaf(x, y):
    draw_circle(x, y, 60, (0, 1, 0))
    draw_circle(x + 50, y, 40, (0, 1, 0))
    draw_circle(x - 50, y, 30, (0, 1, 0))
    draw_circle(x + 50, y - 50, 20, (0, 1, 0))
    draw_circle(x - 50, y + 20, 30, (0, 1, 0))
    draw_circle(x + 50, y + 10, 30, (0, 1, 0))
    draw_circle(x - 50, y + 20, 30, (0, 1, 0))
    draw_circle(x + 50, y + 10, 30, (0, 1, 0))
    draw_circle(x - 50, y, 30, (0, 1, 0))
    draw_circle(x - 40, y - 40, 30, (0, 1, 0))
    draw_circle(x + 30, y + 40, 15, (0, 1, 0))


rain_animation = False
rain_timer = 0
rain_duration = 120 # 5 seconds at 20 FPS
raindrops = [(random.uniform(0, 800), random.uniform(0, 800)) for _ in range(2000)]


def draw_raindrop(x, y):
    glColor3f(0.5, 0.5, 1.0)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y + 3)
    glEnd()
    
# Function to draw sky (gradient background)
is_day = True
def draw_sky():
    glBegin(GL_QUADS)
    if is_day and not rain_animation:  # Day without rain
        glColor3f(0.4, 0.7, 1.0)  # Day sky color (top)
        glVertex2f(0, 600)
        glVertex2f(800, 600)
        glColor3f(0.7, 0.9, 1.0)  # Day sky color (bottom)
    elif not is_day and not rain_animation:  # Night without rain
        glColor3f(0.03, 0.03, 0.2)  # Darker night sky color (top)
        glVertex2f(0, 600)
        glVertex2f(800, 600)
        glColor3f(0.1, 0.1, 0.3)  # Darker night sky color (bottom)
    elif rain_animation:  # Rain (either day or night)
        glColor3f(0.2, 0.2, 0.5)  # Rainy sky color (top)
        glVertex2f(0, 600)
        glVertex2f(800, 600)
        glColor3f(0.3, 0.3, 0.7)  # Rainy sky color (bottom)
    glVertex2f(800, 300)
    glVertex2f(0, 300)
    glEnd()


# Clouds
flower_rotation_angle = 0.0
def draw_cloud(x, y):

    if rain_animation:
        glColor3f(0.5, 0.5, 0.5)  # Dark grey clouds during rain
    else:
        glColor3f(1, 1, 1)  # White clouds (color will be overridden during rain)
    glPushMatrix()
    glRotatef(flower_rotation_angle, 0, 0, 1)
    draw_circle(x, y, 50, (1, 1, 1))
    draw_circle(x + 50, y, 40, (1, 1, 1))
    draw_circle(x - 50, y, 40, (1, 1, 1))
    glPopMatrix()

# Stars
def draw_star(x, y):
    # Drawing a simple star using a point
    glColor3f(1, 1, 1)  # White color for stars
    glPointSize(2.0)  # Adjusting the size of the point
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


star_positions = [(random.uniform(0, 800), random.uniform(800, 400)) for _ in range(100)]


# Function to draw ground (flat surface)
def draw_ground():
    glColor3f(0.0, 0.6, 0.0)  
    glBegin(GL_QUADS)
    glVertex2f(0, 300)
    glVertex2f(800, 300)
    glVertex2f(700, 0)
    glVertex2f(0, 0)
    glEnd()

# Function to draw a simple house
def draw_house(situation):
    # Draw main body of the house
    glColor4f(1.0, 1.0, 0.0, 1.0) 
    glBegin(GL_POLYGON)
    glVertex2d(200, 200)
    glVertex2d(300, 200)
    glVertex2d(300, 250)
    glVertex2d(250, 300)
    glVertex2d(200, 250)
    glVertex2d(200, 200)

    glVertex2d(300, 200)
    glVertex2d(350, 200)
    glVertex2d(350, 250)
    glVertex2d(300, 250)

    glEnd()

    # Draw roof
    glColor3f(1.0, 0.0, 0.0)  # Dark red color for the roof
    glBegin(GL_POLYGON)
    glVertex2d(200, 250)
    glVertex2d(180, 270)
    glVertex2d(250, 340)
    glVertex2d(250, 300)
    glVertex2d(200, 250)
    glEnd()

    glColor3f(0.5, 0.0, 0.0)  # Black color for windows
    glBegin(GL_QUADS)
    glVertex2d(300, 250)
    glVertex2d(310, 270)
    glVertex2d(250, 340)
    glVertex2d(250, 300)
    glVertex2d(300, 250)
    glEnd()

    glColor3f(0.5, 0.0, 0.0)  # Black color for windows
    glBegin(GL_POLYGON)
    glVertex2d(310, 270)
    glVertex2d(350, 270)
    glVertex2d(370, 250)
    glVertex2d(300, 250)
    glVertex2d(310, 270)
    glEnd()

    # Draw windows
    # Window 1
    if situation == "day":
        glColor3f(0.0, 0.0, 0.0)  # Black color for windows
    else:
        glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2d(310, 220)
    glVertex2d(340, 220)
    glVertex2d(340, 240)
    glVertex2d(310, 240)
    glEnd()

    if situation == "day":
        glColor3f(0.0, 0.0, 0.0)  # Black color for windows
    else:
        glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2d(210, 220)
    glVertex2d(230, 220)
    glVertex2d(230, 240)
    glVertex2d(210, 240)
    glEnd()
    if situation == "day":
        glColor3f(0.0, 0.0, 0.0)  # Black color for windows
    else:
        glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2d(275, 220)
    glVertex2d(295, 220)
    glVertex2d(295, 240)
    glVertex2d(275, 240)
    glEnd()

    # Door
    glColor3f(0.0, 0.5, 0.5)  # Black color for windows
    glBegin(GL_QUADS)
    glVertex2d(235, 200)
    glVertex2d(235, 240)
    glVertex2d(265, 240)
    glVertex2d(265, 200)
    glEnd()

    # Door Nob
    glColor3f(1.0, 1.0, 0.5)  # Black color for windows
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(260, 220)
    glEnd()



def draw_bird(x, y):
    glColor3f(0, 0, 0)  # Black color for the bird
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x - 10, y + 10)
    glVertex2f(x, y)
    glVertex2f(x + 10, y + 10)
    glEnd()


# Global variable to hold bird positions
bird_positions = [
    (600, 400), (700, 450), (550, 550),
    (700, 300), (750, 400), (750, 550),
    (800, 450), (900, 500),
    (600, 300), (500, 500)
]
# Global variable to control bird animation
bird_animation = False


def animate_birds():
    global bird_positions
    # Move the birds to the left
    bird_positions = [(x - 2, y) for x, y in bird_positions]


def draw_river():
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 1.0)  # Blue color for water
    glVertex2f(500, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 300)
    glVertex2f(500, 300)
    glEnd()



# Reflection Transformation Function to draw the reflection of the boat
def draw_boat_reflection(x_position, is_day):
    if not is_day:
        return  # Only draw reflection during the day

    # Reflection transformation (mirror across the y-axis at the river level)
    reflection_y = 200  # Level of the river where the reflection occurs
    glColor4f(0.6, 0.3, 0.1, 0.05)
    glBegin(GL_POLYGON)
    glVertex2f(x_position, 2 * reflection_y - 270)
    glVertex2f(x_position + 45, 2 * reflection_y - 220)
    glVertex2f(x_position + 110, 2 * reflection_y - 220)
    glVertex2f(x_position + 150, 2 * reflection_y - 270)
    glVertex2f(x_position, 2 * reflection_y - 270)
    glEnd()

    # Drawing the upper part reflection with reduced opacity and slight color modification
    glColor4f(0.3, 0.75, 0.7, 0.1)
    glBegin(GL_POLYGON)
    glVertex2f(x_position + 75, 2 * reflection_y - 290)
    glVertex2f(x_position + 75, 2 * reflection_y - 330)
    glVertex2f(x_position + 150, 2 * reflection_y - 330)
    glVertex2f(x_position + 150, 2 * reflection_y - 290)
    glVertex2f(x_position + 75, 2 * reflection_y - 290)
    glEnd()

    # Additional reflection details
    glColor4f(0.5, 0.5, 0.5, 0.05)
    glBegin(GL_QUADS)
    glVertex2f(x_position + 75, 2 * reflection_y - 270)
    glVertex2f(x_position + 75, 2 * reflection_y - 330)
    glVertex2f(x_position + 72, 2 * reflection_y - 330)
    glVertex2f(x_position + 72, 2 * reflection_y - 270)
    glEnd()

    draw_circle(x_position + 113, 307 - reflection_y - 15, 13, (1.0, 0.3, 0.3, 0.05))


def draw_boat(x_position, is_day):
    # Draw the base of the boat
    glColor3f(1.0, 0.5, 0.0)
    glBegin(GL_POLYGON)
    glVertex2f(x_position, 270)
    glVertex2f(x_position + 45, 220)
    glVertex2f(x_position + 110, 220)
    glVertex2f(x_position + 150, 270)
    glVertex2f(x_position, 270)

    glEnd()

    # Draw the upper part of the boat
    glColor3f(0.0, 0.9, 0.0)  # Slightly darker shade for the upper part
    glBegin(GL_POLYGON)
    glVertex2f(x_position + 75, 290)
    glVertex2f(x_position + 75, 330)
    glVertex2f(x_position + 150, 330)
    glVertex2f(x_position + 150, 290)
    glVertex2f(x_position + 75, 290)
    glEnd()

    glColor3f(0.0, 0.0, 0.9)  # Green color for the ground
    glBegin(GL_QUADS)
    glVertex2f(x_position + 75, 270)
    glVertex2f(x_position + 75, 330)
    glVertex2f(x_position + 72, 330)
    glVertex2f(x_position + 72, 270)
    glEnd()

    # Green color for the ground
    draw_circle(x_position + 113, 307, 13, (1, 0, 0))

    draw_boat_reflection(x_position, is_day)


boat_position = 550


# Function to draw a simple flower
def draw_flower(x, y):
    # Draw petals using circles
    petal_radius = 10
    petal_color = (1.0, 0.4, 0.4) 
    for angle in range(0, 360, 60):
        petal_x = x + petal_radius * cos(angle * 3.14 / 180)
        petal_y = y + petal_radius * sin(angle * 3.14 / 180)
        draw_circle_X(petal_x, petal_y, petal_radius, petal_color)
    # Draw center of the flower using a circle
    center_radius = 5
    center_color = (1.0, 1.0, 0.0)  # Yellow color
    draw_circle_X(x, y, center_radius, center_color)


# Function to draw the garden with flowers
def draw_garden():
    # Draw flowers at different positions within the specified area
    for x in range(100, 400, 50):
        for y in range(50, 200, 50):
            draw_flower(x, y)


def draw_fruit(x, y, color=(1.0, 0.0, 0.0)):  # Default color is red
    fruit_radius = 5  # You can adjust the size of the fruit
    midpointcircle(x, y, fruit_radius, color)


def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    global is_day, rain_animation, rain_timer, boat_position
    # Draw sky and ground
    draw_sky()
    draw_ground()
    # Draw houses
    draw_house("day")
    global bird_animation
    draw_river()
    # draw_boat(boat_position)
    draw_treeX(70, 250)
    draw_garden()
    draw_fruit(50, 270, color=(1.0, 0.0, 0.0))
    draw_fruit(60, 280, color=(1.0, 0.0, 0.0))

    global rain_timer, rain_animation
    # Rain Scene
    if rain_animation:
        draw_house("night")
        draw_boat(boat_position, is_day=False)
        # Raindrop animation
        global raindrops
        raindrops = [(x, y - 2) for x, y in raindrops]  # Move raindrops downward
        for x, y in raindrops:
            draw_raindrop(x, y)
        rain_timer += 1
        if rain_timer > rain_duration:
            rain_animation = False
            rain_timer = 0
            raindrops = [(random.uniform(0, 800), random.uniform(0, 800)) for _ in range(2000)]
    # Day Scene
    elif is_day:
        midpointcircle(700, 500, 40, (1.0, 0.843, 0.0))
        draw_cloud(500, 450)
        draw_cloud(300, 420)
        draw_cloud(200, 500)
        draw_house("day")
        draw_boat(boat_position, is_day)
    # Night Scene
    else:
        midpointcircle(700, 500, 40, (1, 1, 1))
        for x, y in star_positions:
            draw_star(x, y)
        draw_house("night")
        draw_boat(boat_position, is_day)
    # Birds Animations
    if bird_animation:
        global bird_positions
        bird_positions = [(x - 2, y) for x, y in bird_positions]  # Move birds to the left
        for x, y in bird_positions:
            draw_bird(x, y)
    glutSwapBuffers()

def mouse(button, state, x, y):
    global rain_animation, rain_timer
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not rain_animation:
            rain_animation = True
            rain_timer = 0

def keyboard(key, x, y):
    global is_day, bird_animation, sun_scale, flower_rotation_angle
    global is_day, rain_animation, rain_timer, boat_position
    if key == b'd':
        is_day = not is_day
    if key == b'b':
        bird_animation = not bird_animation
            
    if key == b'm':
        boat_position += 5
    if key == b'n':
        if boat_position < 500:
            boat_position -= 0
        else:
            boat_position -= 5

    if key == b's' or key == b'S':
        # Toggle scaling factor between 1.0 and 1.5 when the "S" key is pressed
        sun_scale = 1.5 if sun_scale == 1.0 else 1.0

    elif key == b'e' or key == b'E':
        # Rotate right
        flower_rotation_angle += 1.0
    elif key == b'q' or key == b'Q':
        # Rotate left
        flower_rotation_angle -= 5.0
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Scenario in the Bengali Countryside")  # window name
glutDisplayFunc(showScreen)
glutMouseFunc(mouse)
glutIdleFunc(showScreen)  # Keep drawing the scene
glutKeyboardFunc(keyboard)
glutMainLoop()
