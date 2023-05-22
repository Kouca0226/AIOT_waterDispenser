import speech_recognition as sr
import time
r = sr.Recognizer()        
# 設定聲音辨識的靈敏度
r.energy_threshold = 2500
r.pause_threshold = 0.5
timeout = 20
def Voice():
    flag1 = time.time()
    flag2 = 0
    while flag2<timeout:           
        flag2 = time.time()-flag1
        print(flag2)
        try:
            # 打開麥克風
            with sr.Microphone() as source:
                print("請開始說話:")
                r.adjust_for_ambient_noise(source, duration=1) #設定環境噪音等級
                audio = r.listen(source,timeout=5,phrase_time_limit=3) #等待語音輸入        
                listen_text = r.recognize_google(audio, language="zh-TW") # 將剛才說的話轉成繁體中文
                print(listen_text)
                
                for char in listen_text:
                    print(char)
                    if char == '3' or char =='三' or char =='h':
                        aa = 3
                        return aa
                    if char == '2' or char =='二' or char =='w':
                        aa = 2
                        return aa
                    if char == '1' or char =='一' or char =='e':
                        aa = 1
                        return aa
        except sr.UnknownValueError:
            print("語音無法辨識\n")
        except sr.WaitTimeoutError:
            print("listening timed out while waiting for phrase to start")
        except sr.RequestError as e:
            print("語音無法辨識{0}\n" .format(e)) 
    else:
        return -99


if __name__ =="__main__":
    print(f'sp:{Voice()}')