from IMU import IMU

# noinspection PyUnresolvedReferences
import explorerhat as eh
l_motor = eh.motor.one
r_motor = eh.motor.two

FORWARD = 1
STOP = 0
REVERSE = -1



class Robot:
    def __init__(self):
        self.l_motor_dir = STOP
        self.r_motor_dir = STOP
        self.target_drive_speed = 50

        self.r_speed_mul = 1
        self.l_speed_mul = 1

        self.MUL_INC = 1.008
        self.MUL_DEC = 0.992

        self.imu = IMU()
        self.imu.init()
        self.imu.calibrate()
        self.angle = 0

        self.gyro_correction_active = False
        self.l_turn_active = False
        self.r_turn_active = False
        self.target_angle = 0

        self.pause_control_loop = False
        self.pause_ack = False

    def set_calib_factor(self, x):
        self.MUL_INC = 1 + x
        self.MUL_DEC = 1 - x
        print(self.MUL_INC, self.MUL_DEC)


    def _update_motors(self):
        l_motor.speed(min(100, self.target_drive_speed * self.l_speed_mul) * self.l_motor_dir)
        r_motor.speed(min(100, self.target_drive_speed * self.r_speed_mul) * self.r_motor_dir)

    def update_loop(self):
        while True:
            self.angle = self.imu.read()
            if self.l_turn_active:
                if self.angle <= self.target_angle:
                    self.l_motor_dir = STOP
                    self.r_motor_dir = STOP
                    self.l_turn_active = False

            if self.r_turn_active:
                if self.angle >= self.target_angle:
                    self.l_motor_dir = STOP
                    self.r_motor_dir = STOP
                    self.r_turn_active = False

            if self.gyro_correction_active:
                if self.angle > 2:
                    self.l_speed_mul = 1
                    self.r_speed_mul = self.r_speed_mul * self.MUL_DEC * abs(self.angle)/5
                elif self.angle < -2:
                    self.r_speed_mul = 1
                    self.l_speed_mul = self.l_speed_mul * self.MUL_DEC * abs(self.angle)/5

            self._update_motors()

            if self.pause_control_loop:
                self.pause_ack = True
                while self.pause_control_loop:
                    pass
                self.pause_ack = False

