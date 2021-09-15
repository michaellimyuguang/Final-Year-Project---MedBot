# this is speech to text
from pocketsphinx import Decoder
import pyaudio
import pyttsx3
import time
import pyaudio

#setup the decoder as hotword detector
#initialise decoder
config = Decoder.default_config()
config.set_string('-hmm', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/en-us')
config.set_string('-dict', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/my_dict.dict')
decoder = Decoder(config)
#add searches
decoder.set_kws('keyword', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/keywords.list')
decoder.set_search('keyword')

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
                    decoder.set_lm_file('lm', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/my_pruned_lm.lm')
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
                print(decoder.hyp().hypstr)
                # print(captured)
                for string in captured:
                    if (r"s" in string) or (r"sil" in string) or (r"NOISE" in string):
                        print(string)
                        captured.remove(string) #remove unnecessary inputs
                full_text = ' '.join(captured)
                print(full_text)
                full_text = full_text.replace("(2)", "")
                full_text = full_text.replace("(3)", "")
                print(full_text)
                ward_idx = full_text.find("WARD")
                bed_idx = full_text.find("BED")
                ward_no = full_text[ward_idx+5]
                bed_no = full_text[bed_idx+4]
                print(ward_no)
                print(bed_no)
                break
