import pyttsx3
engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', 125)


engine.say("Text types in literature form the basic styles of writing. Factual texts merely seek to inform, whereas literary texts seek to entertain or otherwise engage the reader by using creative language and imagery. There are many aspects to literary writing, and many ways to analyse it, but four basic categories are descriptive, narrative, expository, and argumentative. ")

engine.runAndWait()
