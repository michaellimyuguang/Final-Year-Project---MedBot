from gtts import gTTS
import os
import playsound

fh = open("text.txt", "r")

myText = fh.read().replace("\n", " ")

language = 'en'

output = gTTS(text=myText, lang=language, slow=False)

output.save("output.wav")

playsound.playsound('output.wav', True)
