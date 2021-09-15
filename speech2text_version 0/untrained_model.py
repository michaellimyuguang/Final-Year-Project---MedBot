from pocketsphinx import LiveSpeech

for phrase in LiveSpeech():
    print("You said:")
    print(phrase)
