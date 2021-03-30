#include "pid.h"

static float integral_error = 0;
static float prev_error = 0;
static clock_t start_time = 0;

static float Kp = 0, Ki = 0, Kd = 0;
static float low_lim  = 0, high_lim = 0;
static const int weights[] = {-4, -2, 0, 2, 4};

int pid_init_gains(float Kp_input, float Ki_input, float Kd_input) {
    Kp = Kp_input;
    Ki = Ki_input;
    Kd = Kd_input;
    start_time = clock();
    return 0;
}

int pid_set_limits(float low_lim_input, float high_lim_input) {
    low_lim = low_lim_input;
    high_lim = high_lim_input;
    return 0;
}

float pid_clip(float correction) {
    if (correction < low_lim)
        correction =  low_lim;
    if (correction > high_lim)
        correction =  high_lim;
    return correction;
}

float pid_compute_error(int *sensor_data, int size) {
    float error = 0;
    float count = 0;

    for (int idx=0; idx < size; idx++) {
        if(sensor_data[idx] == 1) {
            error += (float)weights[idx];
            count += 1;
        }
    }
    if (count == 0)
        return 0;

    return (error / count);
}

float pid_compute(int *sensor_data, int size) {
    float error = pid_compute_error(sensor_data, size);

    clock_t end_time = clock();
    clock_t diff = end_time - start_time;
    start_time = end_time;

    integral_error += error * diff;
    float derivative_error = (error - prev_error) * diff;

    float correction = Kp*error + Ki*integral_error + Kd*derivative_error;
    correction = pid_clip(correction);
    return correction;
}

