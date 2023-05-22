from pygame import mixer

mixer.init()
mixer.music.load('Hello.mp3')
mixer.music.play(loops=1) #播放一次
