#include <time.h>

int pid_init_gains(float Kp_input, float Ki_input, float Kd_input);
int pid_set_limits(float low_lim_input, float high_lim_input);

float pid_clip(float correction);
float pid_compute_error(int *sensor_data, int size);
float pid_compute(int *sensor_data, int size);