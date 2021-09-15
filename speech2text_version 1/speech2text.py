from pocketsphinx import Decoder
import pyaudio
import pyttsx3
import time

#setup the decoder as hotword detector
#initialise decoder
config = Decoder.default_config()
config.set_string('-hmm', '/home/michaellimyuguang/speech_2_text/en-us')
config.set_string('-dict', '/home/michaellimyuguang/speech_2_text/hotwords.dict')
decoder = Decoder(config)
#add searches
decoder.set_kws('keyword', '/home/michaellimyuguang/speech_2_text/keywords.list')
decoder.set_search('keyword')

import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                captured = [seg.word for seg in decoder.seg()]
                print(captured)

                if decoder.get_search() == 'keyword' and any("MED" in string for string in captured):
                    print("Detected!")
                    #once hotword detected speech captured, change the decoder to work as speech recognition using language model
                    decoder.set_lm_file('lm', '/home/michaellimyuguang/speech_2_text/my_pruned_lm.lm')
                    decoder.set_search('lm')
                    break
                else:
                    #if hotword not detected in in speech captured, continue finding the hotword
                    decoder.set_search('keyword')

                decoder.start_utt()
    else:
        break

#response to user input
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 160)
engine.say('hi, how can i help you?')
engine.runAndWait()
time.sleep(2)

#run speech recognition using language model
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                captured = [seg.word for seg in decoder.seg()]
                print(captured)
                for string in captured:
                    if "<" in string or ">" in string:
                        captured.remove(string) #remove unnecessary inputs
                full_text = ' '.join(captured)
                print(full_text)
                break
