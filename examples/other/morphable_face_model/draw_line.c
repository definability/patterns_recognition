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

void fill_bottom_flat_triangle(float* canvas, double* vertices, int color, int canvas_width) {

    double* top = &vertices[4];
    double* left = 0;
    double* right = 0;

    if (vertices[0] < vertices[2]) {
        left = &vertices[0];
        right = &vertices[2];
    }
    else {
        right = &vertices[0];
        left = &vertices[2];
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

