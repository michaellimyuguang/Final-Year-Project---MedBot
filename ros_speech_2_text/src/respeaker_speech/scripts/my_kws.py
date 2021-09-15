#!/usr/bin/env python

from pocketsphinx import Decoder
import time
import rospy
from std_msgs.msg import String
import pyttsx3

class KWSDetection(object):
    """Class to add keyword spotting functionality"""

    def __init__(self):
        # initializing publisher with buffer size of 10 messages
        self.pub_ = rospy.Publisher("/kws_data", String, queue_size=10)

        # initialize node
        rospy.init_node("kws_control")
        # Call custom function on node shutdown
        rospy.on_shutdown(self.shutdown)

        self.stop_output = False
        self.start_recognizer()

    #we can add in the boolean from navisystem into this function
    def start_recognizer(self):
        #setup the decoder as hotword detector
        #initialise decoder
        config = Decoder.default_config()
        config.set_string('-hmm', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/en-us')
        config.set_string('-dict', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/my_dict.dict')
        self.decoder = Decoder(config)

        #add searches
        self.decoder.set_kws('keyword', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/keywords.list')
        self.decoder.set_search('keyword')

        self.decoder.start_utt()

        #subscribe to audio topic
        rospy.Subscriber("/sphinx_audio", String, self.process_audio)
        rospy.spin()


    def process_audio(self, data):
        # Check if keyword detected
        if not self.stop_output:
            self.decoder.process_raw(data.data, False, False)
            hypothesis = self.decoder.hyp()
            if hypothesis != None:
                #publish output to a topic
                self.pub_.publish("detected!")
                engine = pyttsx3.init()
                rate = engine.getProperty('rate')
                engine.setProperty('rate', 160)
                engine.say('hi, how can i help you?')
                engine.runAndWait()
                time.sleep(2)

                self.decoder.end_utt()

                #restart the kws
                hypothesis = None
                self.decoder.start_utt()

    @staticmethod
    def shutdown():
        """This function is executed on node shutdown."""
        # command executed after Ctrl+C is pressed
        rospy.loginfo("Stop ASRControl")
        rospy.sleep(1)

if __name__ == "__main__":
    KWSDetection()
