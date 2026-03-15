# 1- Continues Screenshot               [Done]
# 2- Blur(meadean filter) or Darken
# 3- OBjct detatction
# 4- object Size detection
# 5- choose small sizes
# 6- Draw rectangle around smal sizes

# Notes, Installation:
# pip install numpy
# pip install pyautogui
# pip install opencv-python
# sudo apt-get install scrot
# sudo apt-get install python3-tk

import time
import tkinter as tk

import cv2
import numpy as np
import pyautogui

# from tkinter import Frame, Label, PhotoImage, Canvas, YES, BOTH

print("Sleeping for 2 seconds...")
time.sleep(2)

# take screenshot using pyautogui
image = pyautogui.screenshot()

# since the pyautogui takes as a
# PIL(pillow) and in RGB we need to
# convert it to numpy array and BGR
# so we can write it to the disk
# image = np.array(image)
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# a_channel = np.ones(image.shape, dtype=float)/2.0
# image = image*a_channel

# writing it to the disk using opencv
cv2.imwrite("image_normal.png", image)

window = tk.Tk()
window.geometry("700x500")
window.attributes("-alpha", 0.5)

frame = tk.Frame(window, width=600, height=400)
frame.pack()
frame.place(anchor="center", relx=0.5, rely=0.5)

greeting = tk.Label(text="Tkinter Fullscreen")
greeting.pack()

# Create a Label Widget to display the text or Image
img = tk.PhotoImage(file="image_normal.png")
label = tk.Label(frame, image=img)
label.pack()

window.attributes("-fullscreen", True)

# canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
# canvas.pack()
# canvas = tk.Canvas(window, width=600, height=600)
canvas = tk.Canvas(window, width=600, height=600)
canvas.pack(expand=tk.YES, fill=tk.BOTH)
rect = canvas.create_rectangle(10, 10, 40, 40, fill="", outline="green", width=3)


def put_image(file_name, image_object):
    global img
    global canvas
    global image
    global rect

    greeting["text"] = file_name
    # If image object exist, write it to file_name
    cv2.imwrite(file_name, image_object)
    img = tk.PhotoImage(file=file_name)
    canvas.create_image(0, -20, image=img, anchor=tk.NW)
    rect = canvas.create_rectangle(10, 10, 40, 40, fill="", outline="green", width=3)


def dilation_image(image, size):
    binr = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((size, size), np.uint8)
    invert = cv2.bitwise_not(binr)
    dilation = cv2.dilate(invert, kernel, iterations=1)
    dilation = cv2.bitwise_not(dilation)


def do_all():
    global img
    global canvas
    global image
    global rect

    image = cv2.imread("image_normal.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binr = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), np.uint8)
    invert = cv2.bitwise_not(binr)
    dilation = cv2.dilate(invert, kernel, iterations=2)
    output = cv2.bitwise_not(dilation)
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        dilation, 4, cv2.CV_32S
    )
    output = cv2.imread("image_normal.png")

    for i in range(0, numLabels):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]
        if area > 500 or h < w:
            continue
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
        componentMask = (labels == i).astype("uint8") * 255

    put_image("image_output.png", output)
    greeting["text"] = "image_output"
    # If image object exist, write it to file_name
    cv2.imwrite("image_output.png", output)
    img = tk.PhotoImage(file="image_output.png")
    canvas.create_image(0, -20, image=img, anchor=tk.NW)
    rect = canvas.create_rectangle(10, 10, 40, 40, fill="", outline="green", width=3)


def onKeyPress(event):
    # text.insert('end', 'You pressed %s\n' % (event.char, ))
    global img
    global canvas
    global image
    global rect

    if event.char == "q":
        do_all()

    elif event.char == "a":
        put_image("image_normal.png", image)
    elif event.char == "e":
        image = cv2.imread("image_normal.png")
        image = cv2.blur(image, (3, 3))
        put_image("image_blur.png", image)
    elif event.char == "f":
        image = cv2.imread("image_blur.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        put_image("image_gray.png", gray)

    elif event.char == "g":
        image = cv2.imread("image_blur.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binr = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
        put_image("image_binary.png", binr)
    elif event.char == "h":
        image = cv2.imread("image_gray.png")
        dilation = dilation_image(image, 2)
        put_image("image_dilation.png", dilation)

    elif event.char == "i":
        image = cv2.imread("image_dilation.png")
        dilation = dilation_image(image, 5)
        put_image("image_dilation.png", dilation)

    elif event.char == "j":
        image = cv2.imread("image_dilation.png")
        image = cv2.bitwise_not(image)
        put_image("image_dilation.png", image)

    elif event.char == "k":
        image = cv2.imread("image_dilation.png")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]
        numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            thresh, 4, cv2.CV_32S
        )

        output = cv2.imread("image_normal.png")
        # loop over the number of unique connected component labels
        for i in range(0, numLabels):
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            area = stats[i, cv2.CC_STAT_AREA]
            (cX, cY) = centroids[i]

            if i == 0:
                text = "examining component {}/{} (background)".format(i + 1, numLabels)
            # otherwise, we are examining an actual connected component
            else:
                text = "examining component {}/{} -> size {}".format(
                    i + 1, numLabels, area
                )

            if area > 500 or h < w:
                continue

            # component
            print("[INFO] {}".format(text))
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)

            componentMask = (labels == i).astype("uint8") * 255

        put_image("image_output.png", output)


def motion(event):
    x, y = event.x, event.y
    print("{}, {}".format(x, y))
    canvas.moveto(rect, x - 10, y - 10)


def task():

    # colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
    # for i in range(5):
    #    print(i)
    #    time.sleep(0.5)
    #    canvas.itemconfig(rect, fill = colors[i])
    # window.destroy()
    pass


do_all()

window.after(2000, task)

window.wait_visibility(window)
# window.wm_attributes('-alpha',0.5)

window.bind("<KeyPress>", onKeyPress)
window.bind("<Motion>", motion)
window.mainloop()
