import time
import numpy as np
from gpiozero import DigitalOutputDevice, Button

from interpolation import discretize_waveform_steps

class Motor():
    def __init__(self, control_pins):
        self.motor_en = DigitalOutputDevice(control_pins[0], initial_value=False)
        self.motor_dir = DigitalOutputDevice(control_pins[1], initial_value=False)
        self.running = True


    def _step(self, direction):
        if direction:  # Away from the motor
            self.motor_dir.off()
        else:  # Towards the motor
            self.motor_dir.on()


        self.motor_en.on()  # Maybe add a delay here to make motor steps more consistent
        #time.sleep(self.on_duration)
        self.motor_en.off()
    
    def step_away(self):
        if self.running:
            self._step(1)


    def step_towards(self):
        if self.running:
            self._step(0)
    
    def estop(self):
        self.motor_en.off()
        self.running = False
        raise RuntimeError("Emergency stop activated. Motor stopped.")




class ShakeTable():
    def __init__(self):
        self.init_gpio()
        self.calibrate()

    def test_func2(self):
        print('Button Pressed')

    def init_gpio(self):
        '''
        Sensor 0 is the close sensor. Sensor 1 is the far sensor. (from the motor)
        Direction 0 is away from the motor. Direction 1 is close to the motor.
        '''
        self.motor_control_pins = [17, 27]
        self.sensor_pins = [19, 26]


        self.motor = Motor(self.motor_control_pins)
        
        self.far_sensor = Button(self.sensor_pins[0], bounce_time=0.05)
        self.near_sensor = Button(self.sensor_pins[1], bounce_time=0.05)

        print("init_gpio")
        #If the plate reaches the sensors, stop the motor from going further
        self.far_sensor.when_pressed = self.motor.estop
        self.near_sensor.when_pressed = self.motor.estop


    def center(self):
        '''
        Moves the shake table to the center position, halfway between the two sensors.
        '''
        if not self.tot_steps:
            self.calibrate()
            return
        
        self.near_sensor.when_pressed = None
        self.far_sensor.when_pressed = None


        while not self.near_sensor.is_pressed:
            self.motor.step_towards()
            time.sleep(0.0001)


        for _ in range(self.tot_steps // 2): # Move to the center position
            self.motor.step_away()
            time.sleep(0.0001)
        
        print("center estop");

        self.near_sensor.when_pressed = self.motor.estop
        self.far_sensor.when_pressed = self.motor.estop


    def calibrate(self):
        '''
        Finds and sets the number of steps between the two sensors and centers the shake table.
        '''
        self.tot_steps = 0
        self.near_sensor.when_pressed = None   # Disable the emergency stop for calibration
        self.far_sensor.when_pressed = None


        while not self.near_sensor.is_pressed:  #Go to the near end range
            self.motor.step_towards()
            time.sleep(0.0001)


        while not self.far_sensor.is_pressed:  #Go to the far end range
            self.motor.step_away()
            time.sleep(0.0001)
            self.tot_steps += 1
        
        for _ in range(self.tot_steps // 2): # Move to the center position
            self.motor.step_towards()
            time.sleep(0.0001)
        
        print("calibrate estop")

        self.near_sensor.when_pressed = self.motor.estop
        self.far_sensor.when_pressed = self.motor.estop




    def run_trajectory(self, times, amplitudes):
        result = discretize_waveform_steps(times, amplitudes)
        if result is None:
            return
       
        direction_array, time_diff_array, end_time_array = result
       
        start_time = time.perf_counter()  # better precision than time.time()
       
        for i, direction in enumerate(direction_array):
            target_time = end_time_array[i]
            current_time = time.perf_counter() - start_time
            wait_time = target_time - current_time
           
            if wait_time > 0:
                time.sleep(wait_time)
           
            if direction == 1:
                self.motor.step_away()
            else:
                self.motor.step_towards()


def test_table_features():
    """
    This function initializes the ShakeTable and calibrates it
    """
    table = ShakeTable()
    table.calibrate()


    print('ShakeTable calibrated with %d steps between sensors.' % table.tot_steps)
    time.sleep(2)

    for _ in range(table.tot_steps//4):
        table.motor.step_away()
        time.sleep(0.0005)
    time.sleep(2)
    print('ShakeTable moved away from the near sensor.')


    table.center()
    print('ShakeTable recentered')

    time.sleep(2)
   

 #   for _ in range(table.tot_steps):
 #       if not table.near_sensor.is_pressed:
 #           table.motor.step_towards()
 #       else:
 #           table.motor.step_away()
 #       time.sleep(0.0002)
        

  
if __name__ == '__main__':
    #test_table_features()
    #Showing natural frequencies
    #sine_test(250, 7.18, 3)
    #sine_test(250, 6.11, 3)
    #sine_test(250, 4.32, 3)
    #sine_test(250, 4.57, 3)
    pass












