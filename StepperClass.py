import RPi.GPIO as GPIO
import time

class Stepper:
    sleepTime = 0.005
    Full_Step = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]
    def __init__(self, pins):
            
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        self.motorPins = pins
        self.total_steps = 0
        
        #inital pin setup
        for pin in self.motorPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, 0)
    
    #moves motor right 1 step by default or a specified number of steps via parameter
    def Move_Clockwise(self, steps=1):
        try:
            for _ in range(steps):   
                for pins in range(4):
                    GPIO.output(self.motorPins[pins], self.__Get_Seq(self.total_steps)[pins])   
                self.total_steps += 1
                time.sleep(Stepper.sleepTime)
        except KeyboardInterrupt:
            GPIO.cleanup()
    
    #Moves motor left 1 step by default or a specified number of steps via parameter
    def Move_CClockwise(self, steps=1):
        try:
            for _ in range(steps):   
                for pins in range(4):
                    GPIO.output(self.motorPins[pins], self.__Get_Seq(self.total_steps)[pins])   
                self.total_steps -= 1
                time.sleep(Stepper.sleepTime)  
        except KeyboardInterrupt:
            GPIO.cleanup()
    
    #Returns the correct sequence to based on how many steps the motor has moved and using remainer to pull sequence
    def __Get_Seq(self, steps: int) -> list:
        return Stepper.Full_Step[steps % 4]
    
    #Simple reset function to set the voltages of the pins to zero when not being used
    def Reset_Pins(self):
        for pin in self.motorPins:
            GPIO.output(pin, 0)
    
    #setting total steps taken to zero resets the standard position for the motor
    def Set_Pos(self):
        self.total_steps = 0
        
    #Tracks steps from orgin the recalls the move function to recenter motor
    def Reset_Pos(self):
        if self.total_steps != 0:
            steps_from_origin = self.total_steps % 200 #200 = 1 revolution steps mod 1 rev = distance from starting pos
            if self.total_steps < 0:
                self.Move_Clockwise(200 - steps_from_origin) #Call doesnt support neg nums so subtract steps from origin from 1 rev
                self.total_steps = 0
            else:
                self.Move_CClockwise(steps_from_origin)
                self.total_steps = 0