# Movement logic for the camera Pi setup
# Worked on by: Chase Hunter
# Currently Complete
from StepperClass import *


class MoverClass:
    def __init__(self):
        self.cameraX = 320
        self.cameraY = 240
        self.arrived = False
        self.pinHor = Stepper([31, 36, 33, 35])
        self.pinVer = Stepper([13, 11, 15, 12])

    # this utilize our detection Ai to find the largest box in our detection because we want to only track
    # the closest person, which in most cases would be the largest box
    def findLargest(self, faces):
        currentLargest = 0
        largestBox = []
        for items in faces:
            size = items[2] * items[3]
            if size > currentLargest:
                currentLargest = size
                largestBox = items
        return largestBox

    # This is the function where we move based on the largest box and then once we are within a threshold we will stay
    # there until the person has moved outside the designated box. Currently is partially incomplete due to waiting
    # on the Pi motors being fully hooked up to our 3D Printed Adaptors
    def move(self, faces):
        x, y, width, height = self.findLargest(faces)
        centerX = x + width / 2
        centerY = y + height / 2
        if (centerX - 5 < self.cameraX < centerX + 5) \
                and (centerY - 5 < self.cameraY < centerY + 5):
            self.arrived = True
        if self.arrived:
            if (centerX - width / 2 > self.cameraX or centerX + width / 2 < self.cameraX) \
                    or (centerY - height / 2 > self.cameraY or centerY + height / 2 < self.cameraY):
                self.arrived = False
        if not self.arrived:
            if self.cameraY < centerY:
                self.pinVer.Move_CClockwise()
            if self.cameraY > centerY:
                self.pinVer.Move_Clockwise()
            if self.cameraX < centerX:
                self.pinHor.Move_Clockwise()
            if self.cameraX > centerX:
                self.pinHor.Move_CClockwise()
