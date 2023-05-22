import cv2
import os, glob
import numpy as np

images = []  #存所有訓練圖形
labels = []  #存所有訓練標籤
labelstr = []  #會員姓名
count = 0  #會員編號索引
dirs = os.listdir('images')  #取得所有資料夾及檔案
for d in dirs:
    print(f'd={d}')
    if os.path.isdir('images/' + d):  #只處理資料夾
        files = glob.glob('images/' + d + '/*.pgm')  #取得資料夾中所有圖檔
        for filename in files:  #逐一處理圖片
            img = cv2.imread(filename, cv2.COLOR_BGR2GRAY)
            images.append(img)
            labels.append(count)  #以數值做為標籤
        labelstr.append(d)  #將姓名加入串列
        count += 1

#建立姓名檔案，在辨識人臉時使用
f = open('member.txt', 'w')
f.write(','.join(labelstr))
f.close()

print('開始建立模型...')
model = cv2.face.LBPHFaceRecognizer_create()  #建立LBPH空模型
model.train(np.asarray(images), np.asarray(labels))  #訓練模型
model.save('faces.yml')  #儲存模型
print('建立模型完成！')
        
        