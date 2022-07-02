# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import numpy as np
from collections import deque

lower = np.array([0,0,0])
upper = np.array([0,0,0])
view = np.zeros((471, 636, 3)) + 255

def setContour(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global lower,upper
        if 10<=x<=60 and 180<=y<=230:
            lower = np.array([110, 100, 100])
            upper = np.array([125, 255, 255])
        elif 10<=x<=60 and 260<=y<=310:
            lower = np.array([160, 100, 84])
            upper = np.array([179, 255, 255])
        elif 10<=x<=60 and 340<=y<=390:
            lower = np.array([40, 70, 100])
            upper = np.array([70, 255, 255])


def setWindow():
    global view
    view = np.zeros((471, 636, 3)) + 255
    view = cv2.rectangle(view, (160, 1), (255, 65), colors[0], -1)
    view = cv2.rectangle(view, (275, 1), (370, 65), colors[1], -1)
    view = cv2.rectangle(view, (390, 1), (485, 65), colors[2], -1)
    view = cv2.rectangle(view, (505, 1), (600, 65), colors[3], -1)

    cv2.putText(view, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(view, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(view, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(view, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(view, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    

    kernel = np.ones((5,5), np.uint8)

    blue_pts = [deque(maxlen=1024)]
    green_pts = [deque(maxlen=1024)]
    red_pts = [deque(maxlen=1024)]
    yellow_pts = [deque(maxlen=1024)]

    blue_ind=0
    green_ind=0
    red_ind=0
    yellow_ind=0

    colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
    colorIndex=0

    setWindow()

    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)


    camera= cv2.VideoCapture(0)

    while True:

        ret,frame = camera.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if not ret:
            break

        cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
        cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
        cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
        cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
        cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
        cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

        cv2.rectangle(frame, (10, 180), (60, 230), (255, 0, 0), -1)
        cv2.rectangle(frame, (10, 260), (60, 310), (0, 0, 255), -1)
        cv2.rectangle(frame, (10, 340), (60, 390), (0, 255, 0), -1)

        cv2.namedWindow('Tracking', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('Tracking',setContour)


        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)

        (cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) > 0:

            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            cv2.circle(frame, (int(x), int(y)), int(radius), (128, 128, 255), 2)
            # Get the moments to calculate the center of the contour (in this case a circle)
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            if center[1] <= 65:
                if 40<= center[0] <= 140 :
                    blue_pts = [deque(maxlen=1024)]
                    green_pts = [deque(maxlen=1024)]
                    red_pts = [deque(maxlen=1024)]
                    yellow_pts = [deque(maxlen=1024)]
                    blue_ind = 0
                    green_ind = 0
                    red_ind = 0
                    yellow_ind = 0
                    setWindow()
                    #view[67:,:,:]=255

                elif 160 <= center[0] <= 255:
                    colorIndex = 0

                elif 275 <= center[0] <= 370:
                    colorIndex = 1

                elif 390 <= center[0] <= 485:
                    colorIndex = 2

                elif 505 <= center[0] <= 600:
                    colorIndex = 3

            else:

                if colorIndex == 0:
                    blue_pts[blue_ind].appendleft(center)

                elif colorIndex == 1:
                    green_pts[green_ind].appendleft(center)

                elif colorIndex == 2:
                    red_pts[red_ind].appendleft(center)

                elif colorIndex == 3:
                    yellow_pts[yellow_ind].appendleft(center)

            points = [blue_pts, green_pts, red_pts, yellow_pts]
            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                        cv2.line(view, points[i][j][k - 1], points[i][j][k], colors[i], 2)

            # Show the frame and the view image
        cv2.imshow("Tracking", frame)
        cv2.imshow("Paint", view)

        # If the 'q' key is pressed, stop the loop
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
