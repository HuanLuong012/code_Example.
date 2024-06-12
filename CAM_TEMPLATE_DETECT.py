import cv2
import time
import datetime
import numpy as np
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_SETTINGS, 1)
print("w,h", w, h)
kernel = np.ones((3, 3), np.int8)


def TemplateMatching(img, temp, threshold):
    pt = False
    h, w = temp.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
    _, maxval, _, maxloc = cv2.minMaxLoc(res)
    print("maxval", maxval)
    if maxval > threshold:
        # print("maxval", maxval, )
        cv2.rectangle(
            img, maxloc, (maxloc[0] + w, maxloc[1] + h), (0, 255, 0), 1)
        cv2.imshow('img template', img)
        pt = True
    return pt, maxloc


path = './img_FT140'
temp = cv2.imread(r"./template.png", cv2.IMREAD_GRAYSCALE)
h_temp, w_temp = temp.shape[:2]
while True:
    ret, frame = cap.read()
    new_frame = []
    if ret:
        new_frame = frame[256:768, 320:960]
        # print(new_frame.shape)
        # new_frame = frame
        cv2.imshow("frame", new_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord(' '):
        Time = datetime.datetime.now()
        cv2.imwrite("./img/" + Time.strftime("%H_%M_%S") +
                    ".png", frame[256:768, 320:960])
    if key == ord('t'):
        new_frame_TemplateMatching = frame[512:768, 320:960]
        gray = cv2.cvtColor(new_frame_TemplateMatching, cv2.COLOR_BGR2GRAY)
        Blur = cv2.GaussianBlur(src=gray, ksize=(3, 3), sigmaX=0, sigmaY=0)

        res, maxloc = TemplateMatching(new_frame_TemplateMatching, temp, 0.2)
        if res == True:

            img_show = new_frame_TemplateMatching[maxloc[1]: maxloc[1] +
                                                  h_temp, maxloc[0]: maxloc[0] + w_temp]
            new_blur = Blur[maxloc[1]: maxloc[1] +
                            h_temp, maxloc[0]: maxloc[0] + w_temp]
            _, Binary = cv2.threshold(new_blur, 80, 255, cv2.THRESH_BINARY)
            opening = cv2.morphologyEx(Binary, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
            cnts, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
            cv2.imshow("closing", closing)
            for cnt in cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                area = cv2.contourArea(cnt)

                if area < 800:
                    continue
                print("area", area)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img_show, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.drawContours(img_show, cnt, -1, (0, 0, 255), 2)
            cv2.imshow('img detect', img_show)
cap.release()
cv2.destroyAllWindows()
