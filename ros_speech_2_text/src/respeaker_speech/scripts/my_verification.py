#!/usr/bin/env python

from pocketsphinx import Decoder
import time
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
import pyttsx3

class Verification(object):
    """Class to verify statements"""

    def __init__(self):
        # initializing publisher with buffer size of 10 messages
        self.pub_ = rospy.Publisher("/position_data", Int16MultiArray, queue_size=10)

        # initialize node
        rospy.init_node("verification_control")
        # Call custom function on node shutdown
        rospy.on_shutdown(self.shutdown)

        self.stop_output = False
        self.speech = None
        self.start_recognizer()


    def start_recognizer(self):
        #setup the decoder as hotword detector
        #initialise decoder
        config = Decoder.default_config()
        config.set_string('-hmm', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/en-us')
        config.set_string('-dict', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/my_dict.dict')
        self.decoder = Decoder(config)

        #add searches
        self.decoder.set_kws('verification', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/verification.list')
        self.decoder.set_search('verification')

        self.decoder.start_utt()

        #subscribe to audio topic
        rospy.Subscriber("/sphinx_audio", String, self.process_position)

        #subscribe to speech_data topic
        rospy.Subscriber("/speech_data", String, self.process_speech)
        rospy.spin()

    def process_speech(self, data1):
        self.speech = data1.data
        print(self.speech)

    def process_position(self, data2):
        if self.speech != None:
            print(type(self.speech))
            print(self.speech)
            # self.decoder.process_raw(data2.data, False, False)



if __name__ == "__main__":
    Verification()
