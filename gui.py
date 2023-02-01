from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import datetime
from StepperClass import *
import moveMent

# Gui file
# dependencies included cv2 and tkinter
win = Tk()
win.title(
    "Security Innovation")
win.configure(bg="gray24")
mover = moveMent.MoverClass()
# up, down, left, right buttons frame
frame1 = Frame(win)
frame1.configure(bg="blue")
frame1.pack(side=LEFT, pady=20, padx=20)

# update directory frame
frame2 = Frame(frame1)
frame2.configure(bg="green")
frame2.pack(side=BOTTOM, pady=20, padx=20)

# snapshot button frame
frame3 = Frame(frame1)
frame3.configure(bg="red")
frame3.pack(side=BOTTOM, pady=20, padx=20)

#stepper w/pins
pinHor = Stepper([31,36,33,35])
pinVer = Stepper([13,11,15,12])

# Our up, down, left, and right buttons.
Button(frame1, text="Up", command=lambda: (pinVer.Move_CClockwise(100)), bg="gray44", font=("Consolas", 20), width=4).pack(side=TOP)
Button(frame1, text="Down", command=lambda: (pinVer.Move_Clockwise(100)),bg="gray44", font=("Consolas", 20), width=4).pack(side=BOTTOM)
Button(frame1, text="Left", command=lambda: (pinHor.Move_CClockwise(100)), bg="gray44", font=("Consolas", 20), width=4).pack(side=LEFT)
Button(frame1, text="Right", command=lambda: (pinHor.Move_Clockwise(100)), bg="gray44", font=("Consolas", 20), width=4).pack(side=RIGHT)

#snapshot button sends us to get_snapshot
Button(frame3, text="Snapshot", command=lambda: get_snapshot(frame), font=("Consolas", 14), width=8).pack(side=BOTTOM, pady=20, padx=20)


# get directory path from user & store for snapshotDir - path to folder
def get_newDir():
    snapshotDir = enterDir.get()
    if(len(snapshotDir) == 0): #if have no choosen a new location to store snapshot we use default
        snapshotDir = "/home/pi/Desktop/snapshotStorage" #default storage location for photos
    return snapshotDir


#our default location: /home/pi/Desktop/snapshotStorage
def get_snapshot(img): #this is where we go when we click "snapshot" in gui
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    now = datetime.datetime.now()
    currentDirectory = get_newDir() + "/Date:" + now.strftime("%Y-%m-%dTime:%H:%M:%S") + ".jpg"
    cv2.imwrite(currentDirectory, img)
    print("Image was saved: DataPath: " + currentDirectory)


# where we enter directory
enterDir = Entry(frame2, width=30)
enterDir.pack(side=TOP, pady=20, padx=20)

# make the actual button
ttk.Button(frame2, text="Update Directory", command=get_newDir).pack(side=BOTTOM)


# Create a Label to capture the Video frames 
label = Label(win)
label.pack(pady=20, padx=20)
cap = cv2.VideoCapture(0)
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

frame = None

# Define function to show frame
def show_frames():
    global frame
    # Get the latest frame and convert into Image
    ret, frame = cap.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)y+h/2
    faces = face.detectMultiScale(frame, 1.3, 3)
    for (index, (x, y, w, h)) in enumerate(faces):
        center = (int(x + w / 2), int(y + h / 2))
        # movement function
        mover.move(faces)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
    
    frame = cv2.circle(frame, (int(640/2),int(480/2)), radius=5, color=(0, 0, 255), thickness=-1)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    label.after(10, show_frames)
                                          

show_frames()
win.mainloop()