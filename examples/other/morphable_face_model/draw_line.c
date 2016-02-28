#include <memory.h>

#define max(x,y) x >= y? x : y
#define min(x,y) x <= y? x : y

void draw_scanline(float* canvas, int y, int left_x, int right_x, int color, int canvas_width) {
    left_x += y*canvas_width;
    right_x += y*canvas_width;
    while (left_x <= right_x) {
        if (canvas[left_x] < color) {
            canvas[left_x] = color;
        }
        left_x++;
    }
}

void fill_bottom_flat_triangle(float* canvas, double* top, double* left, double* right, int color, int canvas_width) {

    if (left[0] > right[0]) {
        double* tmp = left;
        left = right;
        right = tmp;
    }

    float invslope1 = (left[0] - top[0]) / (left[1] - top[1]);
    float invslope2 = (right[0] - top[0]) / (right[1] - top[1]);

    float curx1 = top[0];
    float curx2 = top[0];

    int scanlineY = (int)(.5+top[1]);

    while (scanlineY <= (int)(.5+left[1])) {
        draw_scanline(canvas, scanlineY, (int)(.5+max(curx1, left[0])), (int)(.5+min(curx2, right[0])), color, canvas_width);
        curx1 += invslope1;
        curx2 += invslope2;
        scanlineY++;
    }
}

void fill_top_flat_triangle(float* canvas, double* bottom, double* left, double* right, int color, int canvas_width) {

    if (left[0] > right[0]) {
        double* tmp = left;
        left = right;
        right = tmp;
    }

    float invslope1 = (left[0] - bottom[0]) / (left[1] - bottom[1]);
    float invslope2 = (right[0] - bottom[0]) / (right[1] - bottom[1]);

    float curx1 = bottom[0];
    float curx2 = bottom[0];

    int scanlineY = (int)(.5+bottom[1]);

    while (scanlineY >= (int)(.5+left[1]) - 1) {
        draw_scanline(canvas, scanlineY, (int)(.5+max(curx1, left[0])), (int)(.5+min(curx2, right[0])), color, canvas_width);
        curx1 -= invslope1;
        curx2 -= invslope2;
        scanlineY--;
    }
}

void prepare_triangle(float* canvas, double* vertices, int color, int canvas_width) {

    if ((int)(.5+vertices[3]) == (int)(.5+vertices[5])) {
        fill_top_flat_triangle(canvas, &vertices[0], &vertices[2], &vertices[4],
                               color, canvas_width);
        return;
    }
    else if((int)(.5+vertices[1]) == (int)(.5+vertices[3])) {
        fill_bottom_flat_triangle(canvas, &vertices[0], &vertices[2], &vertices[4],
                                  color, canvas_width);
        return;
    }
    double* middle = (double*)malloc(2 * sizeof(double));
    middle[0] = vertices[0] + (vertices[3] - vertices[1])
                            / (vertices[5] - vertices[1])
                            * (vertices[4] - vertices[0]);
    middle[1] = vertices[3];
    fill_bottom_flat_triangle(canvas, middle, &vertices[2], &vertices[4],
                              color, canvas_width);
    fill_top_flat_triangle(canvas, &vertices[0], middle, &vertices[2],
                           color, canvas_width);
    free(middle);
}

