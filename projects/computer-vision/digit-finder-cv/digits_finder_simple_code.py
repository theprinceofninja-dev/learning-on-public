import cv2
import numpy as np
import pyautogui
import time
import tkinter as tk

print("Sleeping for 2 seconds...")
time.sleep(2)

image    = pyautogui.screenshot()
image    = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
gray     = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binr     = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
kernel   = np.ones((5, 5), np.uint8)
invert   = cv2.bitwise_not(binr)
dilation = cv2.dilate(invert, kernel, iterations=2)
numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilation, 4 , cv2.CV_32S)

output   = cv2.imread('image_normal.png')
for i in range(0, numLabels):
    x = stats[i, cv2.CC_STAT_LEFT   ]
    y = stats[i, cv2.CC_STAT_TOP    ]
    w = stats[i, cv2.CC_STAT_WIDTH  ]
    h = stats[i, cv2.CC_STAT_HEIGHT ]
    area = stats[i, cv2.CC_STAT_AREA]
    if area < 500 and h > w:
        cv2.rectangle(output, (x, y), (x + w, y + h), (255, 255, 0), 3)

window = tk.Tk()
window.attributes('-fullscreen', True)

canvas = tk.Canvas(window)
canvas.pack(expand=tk.YES, fill=tk.BOTH)

cv2.imwrite("image_output.png", output)
img = tk.PhotoImage(file="image_output.png")
canvas.create_image(0, 0, image=img, anchor=tk.NW)

window.wait_visibility(window)
window.mainloop()