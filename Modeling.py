from Mask import x
from Mask import y
from Mask import z
from Mask import allface
import numpy as np
import math
from pyglet.gl import *
from pyglet.window.key import *
from pyglet import image

class Triangle:
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.x3 = x3
        self.y3 = y3
        self.z3 = z3
        self.normal = []

    def count_normals(self):
        x1x2 = self.x1 - self.x2
        y1y2 = self.y1 - self.y2
        z1z2 = self.z1 - self.z2

        x2x3 = self.x2 - self.x3
        y2y3 = self.y2 - self.y3
        z2z3 = self.z2 - self.z3

        wrki = math.sqrt((y1y2 * z2z3 - z1z2 * y2y3) ** 2 + (z1z2 * x2x3 - x1x2 * z2z3) ** 2 + (x1x2 * y2y3 - y1y2 * x2x3) ** 2)

        self.normal.append((y1y2 * z2z3 - z1z2 * y2y3) / wrki)
        self.normal.append((z1z2 * x2x3 - x1x2 * z2z3) / wrki)
        self.normal.append((x1x2 * y2y3 - y1y2 * x2x3) / wrki)




WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
keyboard = KeyStateHandler()
window.push_handlers(keyboard)

size = 1
rot = [0, 0, 0]
pos = [0, 0, 0]
angle_keys = [X, Y, Z]
motion_keys = [A, S, D]
Triangles = []

polygon_modes = [GL_LINE, GL_FILL]
mode = 0


@window.event
def on_text_motion(motion):
    global rot, mode, pos
    r = [(1 if keyboard[k] else 0) for k in angle_keys]
    p = [(1 if keyboard[k] else 0) for k in motion_keys]

    if motion == MOTION_UP:
        for i in range(len(rot)):
            rot[i] = ((rot[i] + 5 * r[i]) % 360)

    if motion == MOTION_DOWN:
        for i in range(len(rot)):
            rot[i] = ((rot[i] - 5 * r[i]) % 360)

    if motion == MOTION_NEXT_PAGE:
        mode = not mode
        glPolygonMode(GL_FRONT_AND_BACK, polygon_modes[mode])

    if motion == MOTION_RIGHT:
        for i in range(len(pos)):
            pos[i] = (pos[i] + p[i])

    if motion == MOTION_LEFT:
        for i in range(len(rot)):
            pos[i] = (pos[i] - p[i])


def make_triangle():
    Triangles.clear()
    for i in range(len(allface)):
        for j in range(len(allface)):
            if allface[i][1] == allface[j][0]:
                for k in range(len(allface)):
                    if allface[k][1] == allface[j][1] and allface[k][0] == allface[i][0]:
                        Triangles.append(Triangle(x[allface[i][0]], y[allface[i][0]], z[allface[i][0]],
                                                  x[allface[i][1]], y[allface[i][1]], z[allface[i][1]],
                                                  x[allface[j][1]], y[allface[j][1]], z[allface[j][1]]))

def normals():
    for i in range(len(Triangles)):
        Triangles[i].count_normals()

def draw_model(pos, rot=None):
    glPushMatrix()
    glTranslatef(0.5, 0.8, 0.5)
    glTranslatef(pos[0], pos[1], pos[2])
    if rot is not None:
        glRotatef(rot[2], 0, 0, 1)
        glRotatef(rot[1], 0, 1, 0)
        glRotatef(rot[0], 1, 0, 0)
    glScalef(size, size, size)

    glRotatef(90, 0, 1, 0)

    glBegin(GL_TRIANGLES)

    for i in range(len(Triangles)):
        glNormal3f(Triangles[i].x1 + Triangles[i].normal[0],
                   Triangles[i].y1 + Triangles[i].normal[1],
                   Triangles[i].z1 + Triangles[i].normal[2])
        glColor3f(0.1, 0.3, 0.6)
        glVertex3f(Triangles[i].x1, Triangles[i].y1, Triangles[i].z1)
        glColor3f(0.4, 0.5, 1)
        glVertex3f(Triangles[i].x2, Triangles[i].y2, Triangles[i].z2)
        glColor3f(0.4, 0.6, 0.7)
        glVertex3f(Triangles[i].x3, Triangles[i].y3, Triangles[i].z3)

    glEnd()
    glPopMatrix()

def draw_normals(pos, rot=None):
    glPushMatrix()
    glTranslatef(0.5, 0.5, 0.5)
    glTranslatef(pos[0], pos[1], pos[2])
    if rot is not None:
        glRotatef(rot[2], 0, 0, 1)
        glRotatef(rot[1], 0, 1, 0)
        glRotatef(rot[0], 1, 0, 0)
    glScalef(size, size, size)

    glRotatef(90, 0, 1, 0)

    glBegin(GL_LINES)

    for i in range(len(Triangles)):
        glColor3f(1, 1, 1)
        glVertex3f(Triangles[i].x1, Triangles[i].y1, Triangles[i].z1)
        glVertex3f(Triangles[i].x1 + Triangles[i].normal[0],
                   Triangles[i].y1 + Triangles[i].normal[1],
                   Triangles[i].z1 + Triangles[i].normal[2])

    glEnd()
    glPopMatrix()

def draw_axes():
    glPushMatrix()
    glTranslatef(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    glColor3f(0, 1, 0)
    glVertex3d(-1, -1, 0)
    glVertex3d(1, -1, 0)
    glColor3f(0, 1, 0)
    glVertex3d(-1, 1, 0)
    glVertex3d(-1, -1, 0)
    glColor3f(0, 1, 0)
    glVertex3d(-1, -1, 0)
    glVertex3d(-1, -1, 2)
    glEnd()
    glPopMatrix()


def config_light():
    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (GLfloat * 4)(0, 0, 0, 1))
    glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, (GLfloat * 4)(-1, 0, -1, 1))

    glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(4, 0, 4, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 4)(0.5, 0.3, 0.5, 1))
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (GLfloat * 3)(-1, 0, -1))
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.02)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT1, GL_POSITION, (GLfloat * 4)(-8, 8, 0, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (GLfloat * 4)(0, 0, 0.8, 1))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (GLfloat * 4)(0, 0, 1, 1))
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, (GLfloat * 3)(2.5, -2, 0))
    glLightfv(GL_LIGHT1, GL_SPOT_CUTOFF, (GLfloat)(25.0))

    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT2, GL_POSITION, (GLfloat * 4)(8, -8, 0, 1))
    glLightfv(GL_LIGHT2, GL_SPECULAR, (GLfloat * 4)(0.5, 0, 0, 1))
    glLightfv(GL_LIGHT2, GL_DIFFUSE, (GLfloat * 4)(1, 0, 0, 1))
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, (GLfloat * 3)(-2.5, 2, 0))
    glLightfv(GL_LIGHT2, GL_SPOT_CUTOFF, (GLfloat)(25.0))
    glEnable(GL_LIGHT2)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, (GLfloat * 3)(1, 0.7, 1))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (GLfloat * 3)(1, 0, 1))
    glMaterialf(GL_FRONT, GL_SHININESS, 16)
    glMaterialfv(GL_FRONT, GL_EMISSION, (GLfloat * 4)(0.01, 0, 0.01, 1))

Mx = (gl.GLfloat * 16)(*[1, 0, 0, -0.2,
                         0, 1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1])

Mz = (gl.GLfloat * 16)(*[1, 0, 0, 0.2,
                         0, 1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1])

My = (gl.GLfloat * 16)(*[1, 0, 0, 0,
                         0, 1, 0, 0.12,
                         0, 0, 1, 0,
                         0, 0, 0, 1])


def set_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -2, 2)
    glMultMatrixf(My)
    glRotatef(45, 0, 1, 0)
    glMultMatrixf(Mz)
    glRotatef(-90, 0, 1, 0)
    glMultMatrixf(Mx)
    glTranslatef(-1, 0, -1)
    glRotatef(-90, 0, 1, 0)


@window.event
def on_draw():
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)

    set_projection()

    glMatrixMode(GL_MODELVIEW)
    glPolygonMode(GL_FRONT_AND_BACK, polygon_modes[mode])

    glLoadIdentity()

    make_triangle()

    normals()
    #draw_axes()
    config_light()
    draw_model(pos, rot)

pyglet.app.run()