from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window_width = 600
window_height = 600
center_x = window_width // 4
center_y = window_height // 4
max_circles = 10  # Maximum number of circles allowed
circles = []  # List to store information about circles [center_x, center_y, radius]
circle_speed = 2.5  # Initial speed of circle growth
paused = False

def draw_circle(center_x, center_y, radius):
    glBegin(GL_POINTS)
    x = radius
    y = 0
    decision = 1 - radius

    while y <= x:
        glVertex2f(center_x + x, center_y + y)
        glVertex2f(center_x - x, center_y + y)
        glVertex2f(center_x + x, center_y - y)
        glVertex2f(center_x - x, center_y - y)
        glVertex2f(center_x + y, center_y + x)
        glVertex2f(center_x - y, center_y + x)
        glVertex2f(center_x + y, center_y - x)
        glVertex2f(center_x - y, center_y - x)

        y += 1
        if decision <= 0:
            decision += 2 * y + 1
        else:
            x -= 1
            decision += 2 * (y - x) + 1

    glEnd()
#======================================
def draw_water_ripple():
    global circle_speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glColor3f(0.0, 0.0, 0.0)  # Set color to black
    
    # Draw the water surface as a rectangle
    glBegin(GL_POLYGON)
    glVertex2f(0, 0)
    glVertex2f(window_width, 0)
    glVertex2f(window_width, window_height)
    glVertex2f(0, window_height)
    glEnd()

    glColor3f(0.0, 1.0, 1.0)  # Set color to white

    for circle in circles:
        draw_circle(circle[0], circle[1], circle[2])
        circle[2] += circle_speed  # Increase circle radius

    glutSwapBuffers()

def update_circle_growth(value):
    glutPostRedisplay()
    if not paused:
        glutTimerFunc(16, update_circle_growth, 0)

def create_circle(x, y):
    global circle_speed
    if len(circles) < max_circles:
        circles.append([x, window_height - y, 1.0])  # Store circle's center and initial radius
        glutPostRedisplay()

def keyboard(key, x, y):
    global paused, circle_speed
    if key == b' ':  # Space key
        paused = not paused
        if not paused:
            glutTimerFunc(16, update_circle_growth, 0)
    elif key == b'\x1b':  # Escape key
        sys.exit(0)
    elif key == b'\x1b':  # Left arrow key
        circle_speed += 0.05
    elif key == b'\x1b':  # Right arrow key
        circle_speed -= 0.05 if circle_speed > 0.05 else 0

def mouse(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        create_circle(x, y)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Water Ripple Animation")

    glutDisplayFunc(draw_water_ripple)
    glutTimerFunc(25, update_circle_growth, 0)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)

    glOrtho(0, window_width, 0, window_height, -1, 1)
    glutMainLoop()

if __name__ == "__main__":
    main()
