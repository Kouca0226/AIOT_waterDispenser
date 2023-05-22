from gtts import gTTS
aaa = "Hello"
tts=gTTS(text=aaa, lang='en-US')
tts.save(aaa+'.mp3')