import pyttsx3

engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', 160)

f = open("text.txt", "r")
text = f.read()
print(text)
f.close()

engine.say(text)

engine.runAndWait()
