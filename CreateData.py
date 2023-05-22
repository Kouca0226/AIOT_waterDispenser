import cv2
import os
from time import sleep

def saveImg(image, index):  #圖片存檔
    filename = 'images/' + name + '/face{:03d}.jpg'.format(index)
    cv2.imwrite(filename, image)

ESC = 27
n = 1
index = 0
total = 100  #人臉取樣總數

name = input('輸入姓名 (使用英文)：')
if os.path.isdir('images/' + name):  #使用姓名做為資料夾名稱
    print('此姓名已存在！')
else:
    os.mkdir('images/' + name)  #建立資料夾
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  #開啟攝影機
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    while n > 0:  #取樣
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(
                frame, 
                (x, y), (x + w, y + h), 
                (0, 255, 0), 3
            )  #框選臉部
            if n%5==0:
                image = gray[y: y + h, x: x + w]
                image = cv2.resize(image, (400, 400))  #存檔圖片大小
                saveImg(image, index)
                #sleep(0.1)
                index += 1
                if index >= total:
                    print('取樣完成！')
                    n = -1  #離開迴圈
                    break
            n+=1
        cv2.imshow('video', frame)
        if cv2.waitKey(1) == 27:
            cap.release()  #關閉cam
            cv2.destroyAllWindows()
            break

