import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import pi as PI

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    """glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()"""


class Main(object):
    def __init__(self):
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

        glTranslatef(0.0,0.0, -5)

    def input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
        #check pressed keys
        pressed = pygame.key.get_pressed()
        z_move = 0
        y_rot = 0
        if pressed[pygame.K_LEFT]:
            y_rot = -PI/16
            
        if pressed[pygame.K_RIGHT]:
            y_rot = PI/16

        if pressed[pygame.K_UP]:
            z_move = 0.3

        if pressed[pygame.K_DOWN]:
            z_move = -0.3

        return z_move, y_rot

    
    def run(self):
        while True:
            
            z_move, y_rot = self.input()

            x = glGetDoublev(GL_MODELVIEW_MATRIX)#, modelviewMatrix)

            camera_x = x[3][0]
            camera_y = x[3][1]
            camera_z = x[3][2]

            #transform scene
            glRotatef(y_rot, 0, 1, 0)
            glTranslatef(0,0,z_move)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            Cube()
            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == '__main__':
    main = Main()
    main.run()