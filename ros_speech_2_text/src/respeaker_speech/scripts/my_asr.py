#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from pocketsphinx import Decoder
import time
import pyttsx3


class ASR(object):
    """Class for automatic speech recognition"""
    def __init__(self):

        # initializing publisher with buffer size of 10 messages
        self.pub_ = rospy.Publisher("/speech_data", String, queue_size=10)

        # initialize node
        rospy.init_node("asr_control")

        # call custom function on node shutdown
        rospy.on_shutdown(self.shutdown)

        self.in_speech_bf = False
        self.kws = None

        self.start_recognizer()

    def start_recognizer(self):
        #setup the decoder as ASR
        #initialise decoder
        config = Decoder.default_config()
        config.set_string('-hmm', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/en-us')
        config.set_string('-dict', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/my_dict.dict')
        self.decoder = Decoder(config)

        #add searches
        self.decoder.set_lm_file('lm', '/home/michaellimyuguang/ros_speech_2_text/src/respeaker_speech/essential_files/my_pruned_lm.lm')
        self.decoder.set_search('lm')

        self.decoder.start_utt()

        #subscribe to audio topic
        rospy.Subscriber("/sphinx_audio", String, self.process_audio)

        #subscribe to my_kws topic
        rospy.Subscriber("/kws_data", String, self.process_kws)

        rospy.spin()

    def process_kws(self, data1):
        self.kws = data1.data
        print(self.kws)

    def process_audio(self, data2):
        if self.kws == "detected!":
            self.decoder.process_raw(data2.data, False, False)
            if self.decoder.get_in_speech() != self.in_speech_bf:
                self.in_speech_bf = self.decoder.get_in_speech()
                if not self.in_speech_bf:
                    self.decoder.end_utt()
                    if self.decoder.hyp() != None:
                        string = self.decoder.hyp().hypstr
                        string = string.replace("2", "TO", 1)
                        self.pub_.publish(string)
                        self.kws = None

                    self.decoder.start_utt()


    @staticmethod
    def shutdown():
        """This function is executed on node shutdown."""
        # command executed after Ctrl+C is pressed
        rospy.loginfo("Stop ASRControl")
        rospy.sleep(1)

if __name__ == "__main__":
    ASR()
