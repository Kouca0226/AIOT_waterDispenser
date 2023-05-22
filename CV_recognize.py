import cv2
from cvzone.HandTrackingModule import HandDetector
import time
model = cv2.face.LBPHFaceRecognizer_create()
print('Loading training data...')
model.read('faces.yml')
print('Load training data done.')

f = open('member.txt', 'r')  #讀入模型
names = f.readline().split(',')  #讀入姓名存於串列

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
cap = cv2.VideoCapture(0)  #開啟攝影機
detector = HandDetector(detectionCon=0.5, maxHands=2)
cv2.namedWindow('video', cv2.WINDOW_NORMAL)

def face():
    OP = -2
    f = -1
    a = 0
    b = 0
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face_img = cv2.resize(gray[y: y + h, x: x + w], (400, 400))  #調整成訓練時大小
            try:
                val = model.predict(face_img)
                print('label:{}, conf:{:.1f}'.format(val[0], val[1]))
                if val[0] != f :
                    f = val[0]
                    a = 0
                elif val[1]<30:
                    a+=1
                if val[1]>50:
                    b+=1
                else:
                    b = 0
                print(f'a = {a}||b = {b}')
            except:
                print('辨識時產生錯誤！')
        cv2.imshow('video', frame)
        if a>20:
            OP =  val[0]
            break
        if b>10:
            OP =  -1
            break
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    print(f'OP={OP}')
    return int(OP)

timeout = 20
def gesture():
    OP = -2
    totalFingersold = -1
    a = 0
    flag1 = time.time()
    flag2 = 0
    while cap.isOpened() and flag2<timeout:
        flag2 = time.time()-flag1
        success, img = cap.read()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            bbox = hand["bbox"]        
            fingers = detector.fingersUp(hand)
            totalFingers = fingers.count(1)
            print(totalFingers)
            msg = str(totalFingers)
            cv2.putText(img, msg, (bbox[0]+200,bbox[1]-30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            if (totalFingers != totalFingersold):
                totalFingersold = totalFingers
                a = 0
            else:
                a+=1
            #print(str(totalFingers) + '\t' + str(totalFingersold) + '\t' + str(a))
        if a>180:
            #print('totalfingers = ' + str(totalFingers))
            OP = totalFingers
            break
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
    if flag2>timeout:
        OP = -99
    return OP

if __name__=="__main__":
    #print(f'gesture = {gesture()}\nface = {face()}')
    print(gesture())
    #face()
    cv2.destroyAllWindows()