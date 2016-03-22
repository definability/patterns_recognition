#include <GLFW/glfw3.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

float rx = 0.f, ry = 0.f, rz = 0.f, last_rotated = 0.f;
static void refresh_rotation() {
    rx = 0.f;
    ry = 0.f;
    rz = 0.f;
}
static void error_callback(int error, const char* description)
{
    fputs(description, stderr);
}
static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GL_TRUE);
    if (key == GLFW_KEY_LEFT && action != GLFW_RELEASE) {
        refresh_rotation();
        ry = -1.f;
        last_rotated += 1.f;
    }
    if (key == GLFW_KEY_RIGHT && action != GLFW_RELEASE) {
        refresh_rotation();
        ry = 1.f;
        last_rotated += 1.f;
    }
    if (key == GLFW_KEY_DOWN && action != GLFW_RELEASE) {
        refresh_rotation();
        rx = 1.f;
        last_rotated += 1.f;
    }
    if (key == GLFW_KEY_UP && action != GLFW_RELEASE) {
        refresh_rotation();
        rx = -1.f;
        last_rotated += 1.f;
    }
    if (key == GLFW_KEY_Z && action != GLFW_RELEASE) {
        refresh_rotation();
        rz = -1.f;
        last_rotated += 1.f;
    }
    if (key == GLFW_KEY_A && action != GLFW_RELEASE) {
        refresh_rotation();
        rz = 1.f;
        last_rotated += 1.f;
    }
    if (action == GLFW_RELEASE) {
        refresh_rotation();
        last_rotated = 0.f;
    }
}
void render_face(float* vertices, float* colors, uint16_t* triangles, int amount) {
    GLFWwindow* window;
    glfwSetErrorCallback(error_callback);
    if (!glfwInit())
        exit(EXIT_FAILURE);
    window = glfwCreateWindow(640, 480, "Simple example", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);
    glfwSetKeyCallback(window, key_callback);
    refresh_rotation();
    while (!glfwWindowShouldClose(window))
    {
        float ratio;
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        ratio = width / (float) height;
        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(-2.f, 2.f, -2.f, 2.f, -2.f, 2.f);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        glRotatef(last_rotated, rx, ry, rz);
        glBegin(GL_TRIANGLES);
        size_t i = 0;
        unsigned short j = 0;
        float r, g, b;
        while (i < amount) {
            j = triangles[i];
            //j = i;
            /*
            r = vertices[3*j];
            g = vertices[3*j + 1];
            b = vertices[3*j + 2];
            */
            r = colors[j];
            g = colors[j];
            b = colors[j];
            /*
            if (vertices[3*j+2] > .95f) {
                glColor3f(1.f, 0.f, 0.f);
            } else {
                glColor3f(r, g, b);
            }
            */
            glColor3f(r, g, b);
            glVertex3f(vertices[3*j], vertices[3*j+1], vertices[3*j+2]);
            i++;
        }
        glEnd();
        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    glfwDestroyWindow(window);
    glfwTerminate();
    exit(EXIT_SUCCESS);
}

