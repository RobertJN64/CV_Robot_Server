from IMU import IMU

# noinspection PyUnresolvedReferences
import explorerhat as eh
l_motor = eh.motor.one
r_motor = eh.motor.two

FORWARD = 1
STOP = 0
REVERSE = -1

MUL_INC = 1.1
MUL_DEC = 0.9

class Robot:
    def __init__(self):
        self.l_motor_dir = STOP
        self.r_motor_dir = STOP
        self.target_drive_speed = 75
        self.r_speed_mul = 1

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

    def _update_motors(self):
        l_motor.speed(self.target_drive_speed * self.l_motor_dir)
        r_motor.speed(self.target_drive_speed * self.r_motor_dir * self.r_speed_mul)

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
                    self.r_speed_mul *= MUL_DEC
                elif self.angle < 2:
                    self.r_speed_mul *= MUL_INC

            self._update_motors()

            if self.pause_control_loop:
                self.pause_ack = True
                while self.pause_control_loop:
                    pass
                self.pause_ack = False

