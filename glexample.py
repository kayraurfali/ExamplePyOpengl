from ctypes import c_void_p
from glfw.GLFW import *
from OpenGL import *
from OpenGL.GL import *
from OpenGL.arrays.arraydatatype import ArrayDatatype
import glm
import numpy as np
from shader import Shader

width = 1280
height = 720
forward = False
back = False

aspect = GLfloat(width / height)

def OnKeyPressed(key):
    if key == GLFW_KEY_W:
        global forward 
        forward = True
    elif key == GLFW_KEY_S:
        global back
        back = True

def OnKeyReleased(key):
    global forward, back
    if key == GLFW_KEY_W:
        forward = False
    elif key == GLFW_KEY_S:
        back = False

def OnKeyEvent(_, key, scancode, action, mods):
    if action == GLFW_PRESS:
        OnKeyPressed(key)
    if action == GLFW_RELEASE:
        OnKeyReleased(key)

glfwInit()

window = glfwCreateWindow(width, height, "Deneme", None, None)
glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

glfwMakeContextCurrent(window)
glfwSetKeyCallback(window, OnKeyEvent)
glClearColor(0.3, 0.534, 0.12, 1.0)

vert_shader = """
#version 330 core

layout (location = 0) in vec3 aPos;

uniform mat4 pv;
uniform mat4 model;

void main()
{
    gl_Position = pv * model * vec4(aPos, 1.0);
}
"""

frag_shader = """
#version 330 core

out vec4 FragColor;

void main()
{
    FragColor = vec4(0.2452, 0.47, 0.95, 1.0);
} 
"""

s = Shader()
s.create_program(vert_shader, frag_shader)

vertices = np.array([
     0.5,  0.5, 0.0,
     0.5, -0.5, 0.0,
    -0.5, -0.5, 0.0,
    -0.5,  0.5, 0.0
], dtype=np.float32)

indices = np.array([
    0, 1, 3,   
    1, 2, 3 
], dtype=np.uint32)

vao = glGenVertexArrays(1)

vbo = glGenBuffers(1)
# ebo = glGenBuffers(1)

glBindVertexArray(vao)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), c_void_p(0))
glEnableVertexAttribArray(0)

model = glm.mat4(1.0)
view = glm.lookAt(
    glm.vec3(0.0, 0.0, -3.0),
    glm.vec3(0.0, 0.0, 0.0),
    glm.vec3(0.0, 1.0, 0.0)
)
projection = glm.perspective(glm.radians(60.0),float(width)/float(height),0.1,1000.0)

pv = projection * view

def Move():
    global model
    if forward:
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.01))
    if back:
        model = glm.translate(model, glm.vec3(0.0, 0.0, -0.01))

while (not glfwWindowShouldClose(window)):
    glClear(GL_COLOR_BUFFER_BIT)

    Move()
    s.Use()
    glBindVertexArray(vao)
    glUniformMatrix4fv(glGetUniformLocation(s.m_ProgramId, "pv"), 1, GL_FALSE, glm.value_ptr(pv))
    glUniformMatrix4fv(glGetUniformLocation(s.m_ProgramId, "model"), 1, GL_FALSE, glm.value_ptr(model))
    glDrawArrays(GL_TRIANGLES, 0, 6)
    
    glfwSwapBuffers(window)
    glfwPollEvents()

glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
s.Destroy()