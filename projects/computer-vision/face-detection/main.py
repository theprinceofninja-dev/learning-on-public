import cv2
import mediapipe as mp
from playsound import playsound

t = input()
if t == "1":
    playsound("/home/*******/Music/SFX/sm64_mario_boing.wav")
if t == "2":
    playsound("/home/*******/Music/SFX/mixkit-airport-announcement-ding-1569.wav")
exit()

cap = cv2.VideoCapture(0)
# mpHands = mp.solutions.hands
mpHands = mp.solutions.face_mesh
# hands = mpHands.Hands()
hands = mpHands.FaceMesh()
mpDraw = mp.solutions.drawing_utils

frame = 0
returned = False
while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    # checking whether a hand is detected
    # if results.multi_hand_landmarks:
    found = False
    if results.multi_face_landmarks:
        # for handLms in results.multi_hand_landmarks:  # working with each hand
        for handLms in results.multi_face_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 10:
                    cv2.circle(image, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    cx10, cy10 = cx, cy
                    found = True
                    # print((cx, cy))

            # mpDraw.draw_landmarks(image, handLms, mpHands.FACEMESH_CONTOURS)
    cv2.imshow("Output", image)
    cv2.moveWindow("Output", cx10, cy10)
    cv2.waitKey(1)
    # continue
    if not found and frame % 10 == 0:
        print("Where are you?")
        playsound("/home/*******/Music/SFX/beep-07a.wav")
        returned = True
    elif not found:
        print(f"Where are you {frame}\r")
    else:  # found
        if returned:
            playsound("/home/*******/Music/SFX/sm64_mario_boing.wav")
            returned = False
    frame += 1
